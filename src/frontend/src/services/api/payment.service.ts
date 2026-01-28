import apiService from './api.service';

interface PaymentMethod {
  id: string;
  user_id: string;
  type: string;
  provider: string;
  last_four: string;
  expiry_date?: string;
  brand?: string;
  is_default: boolean;
  status: string;
  created_at: string;
}

interface Payment {
  id: string;
  user_id: string;
  subscription_id?: string;
  amount: number;
  currency: string;
  status: string;
  payment_method_id: string;
  payment_method: PaymentMethod;
  transaction_id: string;
  created_at: string;
  updated_at: string;
}

interface AddPaymentMethodData {
  type: string;
  provider: string;
  details: {
    number?: string;
    expiry_month?: number;
    expiry_year?: number;
    cvc?: string;
    email?: string;
    wallet_address?: string;
    bank_account?: {
      account_number: string;
      routing_number: string;
      account_holder_name: string;
    };
  };
  set_as_default?: boolean;
}

interface CreatePaymentData {
  amount: number;
  currency: string;
  payment_method_id: string;
  subscription_id?: string;
  description?: string;
}

interface PaymentHistoryFilter {
  start_date?: string;
  end_date?: string;
  status?: string;
  limit?: number;
  offset?: number;
}

class PaymentService {
  /**
   * 获取用户的支付方式
   * @returns 支付方式列表
   */
  async getPaymentMethods(): Promise<PaymentMethod[]> {
    return apiService.get<PaymentMethod[]>('/commerce/payments/methods');
  }

  /**
   * 添加新的支付方式
   * @param data 支付方式数据
   * @returns 创建的支付方式
   */
  async addPaymentMethod(data: AddPaymentMethodData): Promise<PaymentMethod> {
    return apiService.post<PaymentMethod>('/commerce/payments/methods', data);
  }

  /**
   * 删除支付方式
   * @param paymentMethodId 支付方式ID
   * @returns 删除结果
   */
  async deletePaymentMethod(paymentMethodId: string): Promise<{ message: string }> {
    return apiService.delete<{ message: string }>(`/commerce/payments/methods/${paymentMethodId}`);
  }

  /**
   * 设置默认支付方式
   * @param paymentMethodId 支付方式ID
   * @returns 更新结果
   */
  async setDefaultPaymentMethod(paymentMethodId: string): Promise<PaymentMethod> {
    return apiService.put<PaymentMethod>(`/commerce/payments/methods/${paymentMethodId}/default`);
  }

  /**
   * 创建支付
   * @param data 支付数据
   * @returns 创建的支付
   */
  async createPayment(data: CreatePaymentData): Promise<Payment> {
    return apiService.post<Payment>('/commerce/payments', data);
  }

  /**
   * 获取支付历史
   * @param filter 过滤条件
   * @returns 支付列表
   */
  async getPaymentHistory(filter?: PaymentHistoryFilter): Promise<Payment[]> {
    return apiService.get<Payment[]>('/commerce/payments/history', { params: filter });
  }

  /**
   * 获取支付详情
   * @param paymentId 支付ID
   * @returns 支付详情
   */
  async getPaymentDetails(paymentId: string): Promise<Payment> {
    return apiService.get<Payment>(`/commerce/payments/${paymentId}`);
  }

  /**
   * 获取默认支付方式
   * @returns 默认支付方式
   */
  async getDefaultPaymentMethod(): Promise<PaymentMethod | null> {
    try {
      const methods = await this.getPaymentMethods();
      return methods.find(method => method.is_default) || null;
    } catch (error) {
      console.error('获取默认支付方式失败:', error);
      return null;
    }
  }
}

export const paymentService = new PaymentService();
export default paymentService;
export type { PaymentMethod, Payment, AddPaymentMethodData, CreatePaymentData, PaymentHistoryFilter };
