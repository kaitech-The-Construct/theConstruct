import { writable, get } from 'svelte/store';
import { user, isAuthenticated } from './auth';

const API_URL = 'http://localhost:8000/notifications';

export interface Notification {
	notification_id?: string;
	id?: string;
	title?: string;
	message?: string;
	type?: string;
	priority?: string;
	is_read?: boolean;
	read?: boolean;
	created_at?: string;
	[key: string]: any;
}

export interface SystemAlert {
	alert_id?: string;
	id?: string;
	title: string;
	message: string;
	severity: string;
	created_at?: string;
	[key: string]: any;
}

function createNotificationStore() {
	const { subscribe, set, update } = writable<{
		notifications: Notification[];
		activeAlerts: SystemAlert[];
		unreadCount: number;
		isLoading: boolean;
		error: string | null;
	}>({
		notifications: [],
		activeAlerts: [],
		unreadCount: 0,
		isLoading: false,
		error: null
	});

	return {
		subscribe,

		init: () => {
			// Setup listener for auth changes
			isAuthenticated.subscribe((isAuth) => {
				const currentUser = get(user);
				if (isAuth && currentUser) {
					notificationStore.loadNotifications();
					notificationStore.loadActiveAlerts();
				} else {
					// Clear notifications on logout
					set({
						notifications: [],
						activeAlerts: [],
						unreadCount: 0,
						isLoading: false,
						error: null
					});
				}
			});
		},

		loadNotifications: async () => {
			const isAuth = get(isAuthenticated);
			const currentUser = get(user);
			if (!isAuth || !currentUser) return;

			const userId = currentUser.id || currentUser.username || 'default_user';

			update((s) => ({ ...s, isLoading: true, error: null }));
			try {
				const response = await fetch(`${API_URL}/history/${userId}?limit=20`);
				if (!response.ok) throw new Error('Failed to load notifications');
				const data = await response.json();

				const notifications = data.notifications || data.history || [];
				const unreadCount = notifications.filter((n: any) => !n.is_read && !n.read).length;

				update((s) => ({ ...s, notifications, unreadCount, isLoading: false }));
			} catch (err: any) {
				update((s) => ({ ...s, isLoading: false, error: err.message }));
			}
		},

		loadActiveAlerts: async () => {
			try {
				const response = await fetch(`${API_URL}/alerts/active`);
				if (!response.ok) throw new Error('Failed to load alerts');
				const data = await response.json();

				const activeAlerts = data.active_alerts || data.alerts || [];
				update((s) => ({ ...s, activeAlerts }));
			} catch (err: any) {
				console.error('Error loading active alerts:', err);
			}
		},

		markAsRead: async (notificationId: string) => {
			const isAuth = get(isAuthenticated);
			const currentUser = get(user);
			if (!isAuth || !currentUser) return;

			const userId = currentUser.id || currentUser.username || 'default_user';

			try {
				const response = await fetch(`${API_URL}/read/${notificationId}?user_id=${userId}`, {
					method: 'PUT'
				});

				if (response.ok) {
					update((s) => {
						const updatedNotifications = s.notifications.map((n) =>
							n.id === notificationId || n.notification_id === notificationId
								? { ...n, is_read: true, read: true }
								: n
						);
						const unreadCount = updatedNotifications.filter((n) => !n.is_read && !n.read).length;
						return { ...s, notifications: updatedNotifications, unreadCount };
					});
				}
			} catch (err: any) {
				console.error('Error marking notification as read:', err);
			}
		},

		dismissAlert: async (alertId: string) => {
			try {
				const response = await fetch(`${API_URL}/alerts/${alertId}/dismiss`, {
					method: 'PUT'
				});

				if (response.ok) {
					update((s) => {
						const activeAlerts = s.activeAlerts.filter(
							(a) => a.id !== alertId && a.alert_id !== alertId
						);
						return { ...s, activeAlerts };
					});
				}
			} catch (err: any) {
				console.error('Error dismissing alert:', err);
			}
		}
	};
}

export const notificationStore = createNotificationStore();
