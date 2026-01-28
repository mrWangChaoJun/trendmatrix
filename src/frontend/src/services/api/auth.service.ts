import apiService from './api.service';

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    username: string;
    email: string;
    role: string;
  };
}

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
}

class AuthService {
  /**
   * 用户注册
   * @param data 注册数据
   * @returns 认证响应
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    return apiService.post<AuthResponse>('/auth/register', data);
  }

  /**
   * 用户登录
   * @param data 登录数据
   * @returns 认证响应
   */
  async login(data: LoginData): Promise<AuthResponse> {
    return apiService.post<AuthResponse>('/auth/login', data);
  }

  /**
   * 用户登出
   * @returns 登出响应
   */
  async logout(): Promise<{ message: string }> {
    return apiService.post<{ message: string }>('/auth/logout');
  }

  /**
   * 刷新令牌
   * @returns 认证响应
   */
  async refreshToken(): Promise<AuthResponse> {
    return apiService.post<AuthResponse>('/auth/refresh');
  }

  /**
   * 获取当前用户信息
   * @returns 用户信息
   */
  async getCurrentUser(): Promise<User> {
    return apiService.get<User>('/auth/me');
  }

  /**
   * 保存认证信息到本地存储
   * @param response 认证响应
   */
  saveAuthData(response: AuthResponse): void {
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('user', JSON.stringify(response.user));
  }

  /**
   * 清除本地存储的认证信息
   */
  clearAuthData(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  /**
   * 检查用户是否已认证
   * @returns 是否已认证
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  /**
   * 获取当前用户
   * @returns 用户信息或 null
   */
  getCurrentUserFromStorage(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }
}

export const authService = new AuthService();
export default authService;
export type { RegisterData, LoginData, AuthResponse, User };
