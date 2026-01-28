import { defineStore } from 'pinia';
import { subscriptionService, SubscriptionPlan, Subscription, CreateSubscriptionData, UpdateSubscriptionData } from '../services/api/subscription.service';

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    plans: [] as SubscriptionPlan[],
    subscriptions: [] as Subscription[],
    currentSubscription: null as Subscription | null,
    loading: false,
    error: null as string | null,
  }),

  getters: {
    subscriptionPlans: (state) => state.plans,
    userSubscriptions: (state) => state.subscriptions,
    activeSubscription: (state) => state.currentSubscription,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
    errorMessage: (state) => state.error,
    hasActiveSubscription: (state) => !!state.currentSubscription && state.currentSubscription.status === 'active',
  },

  actions: {
    /**
     * 获取订阅计划
     */
    async fetchSubscriptionPlans() {
      this.loading = true;
      this.error = null;

      try {
        this.plans = await subscriptionService.getSubscriptionPlans();
        return this.plans;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取订阅计划失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 获取用户订阅
     */
    async fetchUserSubscriptions() {
      this.loading = true;
      this.error = null;

      try {
        this.subscriptions = await subscriptionService.getUserSubscriptions();
        this.currentSubscription = this.subscriptions.find(sub => sub.status === 'active') || null;
        return this.subscriptions;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取用户订阅失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 获取当前订阅
     */
    async fetchCurrentSubscription() {
      this.loading = true;
      this.error = null;

      try {
        this.currentSubscription = await subscriptionService.getCurrentSubscription();
        return this.currentSubscription;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取当前订阅失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 创建新订阅
     */
    async createSubscription(data: CreateSubscriptionData) {
      this.loading = true;
      this.error = null;

      try {
        const subscription = await subscriptionService.createSubscription(data);
        this.subscriptions.push(subscription);
        this.currentSubscription = subscription;
        return subscription;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '创建订阅失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 更新订阅
     */
    async updateSubscription(subscriptionId: string, data: UpdateSubscriptionData) {
      this.loading = true;
      this.error = null;

      try {
        const updatedSubscription = await subscriptionService.updateSubscription(subscriptionId, data);
        const index = this.subscriptions.findIndex(sub => sub.id === subscriptionId);
        if (index !== -1) {
          this.subscriptions[index] = updatedSubscription;
          if (updatedSubscription.status === 'active') {
            this.currentSubscription = updatedSubscription;
          }
        }
        return updatedSubscription;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '更新订阅失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 取消订阅
     */
    async cancelSubscription(subscriptionId: string) {
      this.loading = true;
      this.error = null;

      try {
        await subscriptionService.cancelSubscription(subscriptionId);
        const index = this.subscriptions.findIndex(sub => sub.id === subscriptionId);
        if (index !== -1) {
          this.subscriptions[index].status = 'cancelled';
          if (this.currentSubscription?.id === subscriptionId) {
            this.currentSubscription = null;
          }
        }
      } catch (error: any) {
        this.error = error.response?.data?.detail || '取消订阅失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 获取订阅使用统计
     */
    async getSubscriptionUsage(subscriptionId: string) {
      this.loading = true;
      this.error = null;

      try {
        const usage = await subscriptionService.getSubscriptionUsage(subscriptionId);
        return usage;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取订阅使用统计失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 清除错误信息
     */
    clearError() {
      this.error = null;
    },

    /**
     * 重置状态
     */
    reset() {
      this.plans = [];
      this.subscriptions = [];
      this.currentSubscription = null;
      this.error = null;
    },
  },
});
