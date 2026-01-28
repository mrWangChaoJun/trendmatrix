import { defineStore } from 'pinia';
import { paymentService, PaymentMethod, Payment, AddPaymentMethodData, CreatePaymentData, PaymentHistoryFilter } from '../services/api/payment.service';

export const usePaymentStore = defineStore('payment', {
  state: () => ({
    paymentMethods: [] as PaymentMethod[],
    payments: [] as Payment[],
    defaultPaymentMethod: null as PaymentMethod | null,
    loading: false,
    error: null as string | null,
  }),

  getters: {
    userPaymentMethods: (state) => state.paymentMethods,
    paymentHistory: (state) => state.payments,
    primaryPaymentMethod: (state) => state.defaultPaymentMethod,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
    errorMessage: (state) => state.error,
    hasPaymentMethods: (state) => state.paymentMethods.length > 0,
  },

  actions: {
    /**
     * 获取支付方式
     */
    async fetchPaymentMethods() {
      this.loading = true;
      this.error = null;

      try {
        this.paymentMethods = await paymentService.getPaymentMethods();
        this.defaultPaymentMethod = this.paymentMethods.find(method => method.is_default) || null;
        return this.paymentMethods;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取支付方式失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 添加支付方式
     */
    async addPaymentMethod(data: AddPaymentMethodData) {
      this.loading = true;
      this.error = null;

      try {
        const paymentMethod = await paymentService.addPaymentMethod(data);
        this.paymentMethods.push(paymentMethod);
        if (data.set_as_default || this.paymentMethods.length === 1) {
          this.defaultPaymentMethod = paymentMethod;
        }
        return paymentMethod;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '添加支付方式失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 删除支付方式
     */
    async deletePaymentMethod(paymentMethodId: string) {
      this.loading = true;
      this.error = null;

      try {
        await paymentService.deletePaymentMethod(paymentMethodId);
        this.paymentMethods = this.paymentMethods.filter(method => method.id !== paymentMethodId);
        if (this.defaultPaymentMethod?.id === paymentMethodId) {
          this.defaultPaymentMethod = this.paymentMethods[0] || null;
        }
      } catch (error: any) {
        this.error = error.response?.data?.detail || '删除支付方式失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 设置默认支付方式
     */
    async setDefaultPaymentMethod(paymentMethodId: string) {
      this.loading = true;
      this.error = null;

      try {
        const updatedMethod = await paymentService.setDefaultPaymentMethod(paymentMethodId);
        this.paymentMethods = this.paymentMethods.map(method => ({
          ...method,
          is_default: method.id === paymentMethodId,
        }));
        this.defaultPaymentMethod = updatedMethod;
        return updatedMethod;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '设置默认支付方式失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 获取支付历史
     */
    async fetchPaymentHistory(filter?: PaymentHistoryFilter) {
      this.loading = true;
      this.error = null;

      try {
        this.payments = await paymentService.getPaymentHistory(filter);
        return this.payments;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取支付历史失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 创建支付
     */
    async createPayment(data: CreatePaymentData) {
      this.loading = true;
      this.error = null;

      try {
        const payment = await paymentService.createPayment(data);
        this.payments.unshift(payment);
        return payment;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '创建支付失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 获取支付详情
     */
    async fetchPaymentDetails(paymentId: string) {
      this.loading = true;
      this.error = null;

      try {
        const payment = await paymentService.getPaymentDetails(paymentId);
        const index = this.payments.findIndex(p => p.id === paymentId);
        if (index !== -1) {
          this.payments[index] = payment;
        } else {
          this.payments.unshift(payment);
        }
        return payment;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取支付详情失败';
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
      this.paymentMethods = [];
      this.payments = [];
      this.defaultPaymentMethod = null;
      this.error = null;
    },
  },
});
