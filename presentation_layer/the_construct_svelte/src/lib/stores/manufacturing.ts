import { writable } from 'svelte/store';

const API_URL = 'http://localhost:8000/manufacturing'; // Adjust as needed

export interface RFQ {
	id?: string;
	part_name: string;
	quantity: number;
	specifications: string;
	status?: string;
}

export interface Order {
	order_id: string;
	status: string;
	data?: any;
}

export interface Milestone {
	id: string;
	description: string;
	status: string;
	payment_amount: number;
	paid: boolean;
	payment_tx_hash?: string;
}

function createManufacturingStore() {
	const { subscribe, set, update } = writable<{
		orders: Order[];
		activeOrder: Order | null;
		milestones: Milestone[];
		isLoading: boolean;
		error: string | null;
	}>({
		orders: [],
		activeOrder: null,
		milestones: [],
		isLoading: false,
		error: null
	});

	return {
		subscribe,

		submitRFQ: async (rfqData: RFQ) => {
			update((s) => ({ ...s, isLoading: true, error: null }));
			try {
				const response = await fetch(`${API_URL}/rfq`, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify(rfqData)
				});
				if (!response.ok) throw new Error('Failed to submit RFQ');
				const data = await response.json();
				update((s) => ({ ...s, isLoading: false }));
				return data;
			} catch (err: any) {
				update((s) => ({ ...s, isLoading: false, error: err.message }));
				throw err;
			}
		},

		loadOrder: async (orderId: string) => {
			update((s) => ({ ...s, isLoading: true, error: null }));
			try {
				const response = await fetch(`${API_URL}/orders/${orderId}`);
				if (!response.ok) throw new Error('Failed to load order');
				const data = await response.json();

				// Also load milestones for this order
				const msResponse = await fetch(`${API_URL}/orders/${orderId}/milestones`);
				const msData = msResponse.ok ? await msResponse.json() : { milestones: [] };

				update((s) => ({
					...s,
					activeOrder: data,
					milestones: msData.milestones || [],
					isLoading: false
				}));
				return data;
			} catch (err: any) {
				update((s) => ({ ...s, isLoading: false, error: err.message }));
				throw err;
			}
		},

		payMilestone: async (orderId: string, milestoneId: string, wallet: string) => {
			update((s) => ({ ...s, isLoading: true, error: null }));
			try {
				const response = await fetch(`${API_URL}/orders/${orderId}/milestones/${milestoneId}/pay`, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ wallet })
				});
				if (!response.ok) throw new Error('Payment failed');
				const data = await response.json();

				// Reload order to get updated milestones
				await manufacturingStore.loadOrder(orderId);

				update((s) => ({ ...s, isLoading: false }));
				return data;
			} catch (err: any) {
				update((s) => ({ ...s, isLoading: false, error: err.message }));
				throw err;
			}
		},

		reset: () =>
			set({ orders: [], activeOrder: null, milestones: [], isLoading: false, error: null })
	};
}

export const manufacturingStore = createManufacturingStore();
