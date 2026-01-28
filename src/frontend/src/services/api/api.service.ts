import localDbService from '../db/local-db.service';

class ApiService {
  // GET 请求 - 使用本地数据库服务
  async get<T = any>(url: string, config?: any): Promise<T> {
    // 根据 URL 路径返回相应的本地数据
    if (url === '/dashboard/metrics') {
      const metrics = await localDbService.getDashboardMetrics();
      return { data: metrics } as T;
    }

    if (url === '/history/signals') {
      const signals = await localDbService.getRecentSignals(config?.params?.limit || 5);
      return { data: { data: signals } } as T;
    }

    if (url === '/solana/projects/hot') {
      const projects = await localDbService.getHotProjects(config?.params?.limit || 5);
      return { data: { projects } } as T;
    }

    if (url.startsWith('/signals/history/trend')) {
      const days = parseInt(url.split('?days=')[1]) || 7;
      const trendData = await localDbService.getSignalTrendData(days);
      return { data: { trend: trendData } } as T;
    }

    if (url.startsWith('/solana/activity/trend')) {
      const days = parseInt(url.split('?days=')[1]) || 7;
      const activityData = await localDbService.getProjectActivityData(days);
      return { data: { trend: activityData } } as T;
    }

    if (url === '/commerce/subscriptions/plans') {
      const plans = await localDbService.getSubscriptionPlans();
      return plans as T;
    }

    if (url === '/commerce/subscriptions') {
      const subscriptions = await localDbService.getUserSubscriptions();
      return subscriptions as T;
    }

    if (url.includes('/commerce/subscriptions/') && url.includes('/usage')) {
      const usage = {
        api_calls: 250,
        signals_generated: 45,
        api_rate_limit: 1000,
        signal_limit: 100,
        usage_percentage: {
          api: 25,
          signals: 45
        }
      };
      return usage as T;
    }

    // 默认返回空数据
    return {} as T;
  }

  // POST 请求 - 使用本地数据库服务
  async post<T = any>(url: string, _data?: any, _config?: any): Promise<T> {
    // 模拟 POST 请求
    if (url === '/commerce/subscriptions') {
      const subscriptions = await localDbService.getUserSubscriptions();
      return subscriptions[0] as T;
    }

    // 默认返回空数据
    return {} as T;
  }

  // PUT 请求 - 使用本地数据库服务
  async put<T = any>(url: string, _data?: any, _config?: any): Promise<T> {
    // 模拟 PUT 请求
    if (url.includes('/commerce/subscriptions/')) {
      const subscriptions = await localDbService.getUserSubscriptions();
      return subscriptions[0] as T;
    }

    // 默认返回空数据
    return {} as T;
  }

  // DELETE 请求 - 使用本地数据库服务
  async delete<T = any>(url: string, _config?: any): Promise<T> {
    // 模拟 DELETE 请求
    if (url.includes('/commerce/subscriptions/')) {
      return { message: 'Subscription cancelled successfully' } as T;
    }

    // 默认返回空数据
    return {} as T;
  }

  // PATCH 请求 - 使用本地数据库服务
  async patch<T = any>(_url: string, _data?: any, _config?: any): Promise<T> {
    // 默认返回空数据
    return {} as T;
  }
}

export const apiService = new ApiService();
export default apiService;
