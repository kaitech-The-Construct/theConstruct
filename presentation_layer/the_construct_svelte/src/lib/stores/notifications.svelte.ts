import { authStore } from './auth.svelte';

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

class NotificationState {
	notifications = $state<Notification[]>([]);
	activeAlerts = $state<SystemAlert[]>([]);
	unreadCount = $state<number>(0);
	isLoading = $state<boolean>(false);
	error = $state<string | null>(null);

	init() {
		$effect.root(() => {
			$effect(() => {
				const isAuth = authStore.isAuthenticated;
				const currentUser = authStore.user;
				if (isAuth && currentUser) {
					this.loadNotifications();
					this.loadActiveAlerts();
				} else {
					this.notifications = [];
					this.activeAlerts = [];
					this.unreadCount = 0;
					this.isLoading = false;
					this.error = null;
				}
			});
		});
	}

	async loadNotifications() {
		const isAuth = authStore.isAuthenticated;
		const currentUser = authStore.user;
		if (!isAuth || !currentUser) return;

		const userId = currentUser.id || currentUser.username || 'default_user';

		this.isLoading = true;
		this.error = null;
		try {
			const response = await fetch(`${API_URL}/history/${userId}?limit=20`);
			if (!response.ok) throw new Error('Failed to load notifications');
			const data = await response.json();

			const newNotifications = data.notifications || data.history || [];
			this.notifications = newNotifications;
			this.unreadCount = newNotifications.filter((n: any) => !n.is_read && !n.read).length;
			this.isLoading = false;
		} catch (err: any) {
			this.isLoading = false;
			this.error = err.message;
		}
	}

	async loadActiveAlerts() {
		try {
			const response = await fetch(`${API_URL}/alerts/active`);
			if (!response.ok) throw new Error('Failed to load alerts');
			const data = await response.json();

			this.activeAlerts = data.active_alerts || data.alerts || [];
		} catch (err: any) {
			console.error('Error loading active alerts:', err);
		}
	}

	async markAsRead(notificationId: string) {
		const isAuth = authStore.isAuthenticated;
		const currentUser = authStore.user;
		if (!isAuth || !currentUser) return;

		const userId = currentUser.id || currentUser.username || 'default_user';

		try {
			const response = await fetch(`${API_URL}/read/${notificationId}?user_id=${userId}`, {
				method: 'PUT'
			});

			if (response.ok) {
				this.notifications = this.notifications.map((n) =>
					n.id === notificationId || n.notification_id === notificationId
						? { ...n, is_read: true, read: true }
						: n
				);
				this.unreadCount = this.notifications.filter((n) => !n.is_read && !n.read).length;
			}
		} catch (err: any) {
			console.error('Error marking notification as read:', err);
		}
	}

	async dismissAlert(alertId: string) {
		try {
			const response = await fetch(`${API_URL}/alerts/${alertId}/dismiss`, {
				method: 'PUT'
			});

			if (response.ok) {
				this.activeAlerts = this.activeAlerts.filter(
					(a) => a.id !== alertId && a.alert_id !== alertId
				);
			}
		} catch (err: any) {
			console.error('Error dismissing alert:', err);
		}
	}
}

export const notificationStore = new NotificationState();