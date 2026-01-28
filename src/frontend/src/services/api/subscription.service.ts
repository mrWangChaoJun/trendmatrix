import apiService from './api.service';

interface SubscriptionPlan {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  billing_cycle: string;
  features: string[];
  api_rate_limit: number;
  signal_limit: number;
}

interface Subscription {
  id: string;
  user_id: string;
  plan_id: string;
  plan: SubscriptionPlan;
  status: string;
  start_date: string;
  end_date: string;
  auto_renew: boolean;
  current_usage: {
    api_calls: number;
    signals_generated: number;
  };
}

interface CreateSubscriptionData {
  plan_id: string;
  payment_method_id?: string;
  auto_renew?: boolean;
}

interface UpdateSubscriptionData {
  plan_id?: string;
  auto_renew?: boolean;
}

class SubscriptionService {
  /**
   * 获取所有订阅计划
   * @returns 订阅计划列表
   */
  async getSubscriptionPlans(): Promise<SubscriptionPlan[]> {
    return apiService.get<SubscriptionPlan[]>('/commerce/subscriptions/plans');
  }

  /**
   * 获取用户的订阅
   * @returns 用户订阅列表
   */
  async getUserSubscriptions(): Promise<Subscription[]> {
    return apiService.get<Subscription[]>('/commerce/subscriptions');
  }

  /**
   * 获取当前活跃订阅
   * @returns 当前订阅
   */
  async getCurrentSubscription(): Promise<Subscription | null> {
    try {
      const subscriptions = await this.getUserSubscriptions();
      return subscriptions.find(sub => sub.status === 'active') || null;
    } catch (error) {
      console.error('获取当前订阅失败:', error);
      return null;
    }
  }

  /**
   * 创建新订阅
   * @param data 订阅数据
   * @returns 创建的订阅
   */
  async createSubscription(data: CreateSubscriptionData): Promise<Subscription> {
    return apiService.post<Subscription>('/commerce/subscriptions', data);
  }

  /**
   * 更新订阅
   * @param subscriptionId 订阅ID
   * @param data 更新数据
   * @returns 更新后的订阅
   */
  async updateSubscription(subscriptionId: string, data: UpdateSubscriptionData): Promise<Subscription> {
    return apiService.put<Subscription>(`/commerce/subscriptions/${subscriptionId}`, data);
  }

  /**
   * 取消订阅
   * @param subscriptionId 订阅ID
   * @returns 取消结果
   */
  async cancelSubscription(subscriptionId: string): Promise<{ message: string }> {
    return apiService.delete<{ message: string }>(`/commerce/subscriptions/${subscriptionId}`);
  }

  /**
   * 获取订阅使用统计
   * @param subscriptionId 订阅ID
   * @returns 使用统计
   */
  async getSubscriptionUsage(subscriptionId: string): Promise<{
    api_calls: number;
    signals_generated: number;
    api_rate_limit: number;
    signal_limit: number;
    usage_percentage: {
      api: number;
      signals: number;
    };
  }> {
    return apiService.get<{
      api_calls: number;
      signals_generated: number;
      api_rate_limit: number;
      signal_limit: number;
      usage_percentage: {
        api: number;
        signals: number;
      };
    }>(`/commerce/subscriptions/${subscriptionId}/usage`);
  }
}

export const subscriptionService = new SubscriptionService();
export default subscriptionService;
export type { SubscriptionPlan, Subscription, CreateSubscriptionData, UpdateSubscriptionData };
