import { defineStore } from 'pinia';
import { authService, User } from '../services/api/auth.service';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null as string | null,
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
    errorMessage: (state) => state.error,
  },

  actions: {
    /**
     * 初始化认证状态
     */
    initializeAuth() {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        try {
          this.user = JSON.parse(userStr);
          this.isAuthenticated = true;
        } catch {
          this.clearAuth();
        }
      }
    },

    /**
     * 用户登录
     */
    async login(email: string, password: string) {
      this.loading = true;
      this.error = null;

      try {
        const response = await authService.login({ email, password });
        authService.saveAuthData(response);
        
        this.user = response.user;
        this.token = response.access_token;
        this.isAuthenticated = true;
        
        return response;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '登录失败，请检查邮箱和密码';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 用户注册
     */
    async register(username: string, email: string, password: string) {
      this.loading = true;
      this.error = null;

      try {
        const response = await authService.register({ username, email, password });
        authService.saveAuthData(response);
        
        this.user = response.user;
        this.token = response.access_token;
        this.isAuthenticated = true;
        
        return response;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '注册失败，请稍后重试';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 用户登出
     */
    async logout() {
      this.loading = true;
      this.error = null;

      try {
        await authService.logout();
      } catch (error) {
        console.error('登出失败:', error);
      } finally {
        this.clearAuth();
        this.loading = false;
      }
    },

    /**
     * 清除认证状态
     */
    clearAuth() {
      authService.clearAuthData();
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      this.error = null;
    },

    /**
     * 获取当前用户信息
     */
    async fetchCurrentUser() {
      if (!this.isAuthenticated) return;

      this.loading = true;
      this.error = null;

      try {
        const user = await authService.getCurrentUser();
        this.user = user;
        localStorage.setItem('user', JSON.stringify(user));
        return user;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取用户信息失败';
        if (error.response?.status === 401) {
          this.clearAuth();
        }
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
  },
});
