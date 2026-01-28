// 数据模型接口
export interface Signal {
  id: string;
  asset: string;
  type: string;
  strength: number;
  timestamp: string;
}

export interface Project {
  id: string;
  name: string;
  category: string;
  score: number;
  change: number;
}

export interface DashboardMetrics {
  total_signals: number;
  active_projects: number;
  market_sentiment: string;
  sentiment_score: number;
  solana_activity: number;
}

export interface ChartData {
  date: string;
  signals: number;
  activity: number;
}

export interface SubscriptionPlan {
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

export interface Subscription {
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

export interface DefiProtocol {
  id: string;
  name: string;
  category: string;
  tvl: number;
  volume_24h: number;
  change_24h: number;
  users: number;
  url: string;
  twitter: string;
  github: string;
}

export interface NftCollection {
  id: string;
  name: string;
  category: string;
  floor_price: number;
  volume_24h: number;
  volume_7d: number;
  change_24h: number;
  holders: number;
  url: string;
  twitter: string;
}

export interface NftMarketMetrics {
  total_collections: number;
  total_volume_24h: number;
  average_floor_price: number;
  top_collections: NftCollection[];
}

export interface NftTrendData {
  date: string;
  volume: number;
  floor_price: number;
}

class LocalDbService {
  /**
   * 获取仪表盘指标
   */
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    // 直接返回测试数据
    return {
      total_signals: 1250,
      active_projects: 42,
      market_sentiment: '看涨',
      sentiment_score: 78,
      solana_activity: 85
    };
  }

  /**
   * 获取最近的信号
   */
  async getRecentSignals(limit: number = 5): Promise<Signal[]> {
    // 直接返回测试数据
    return [
      { id: '1', asset: 'BTC', type: 'trend', strength: 85, timestamp: new Date().toISOString() },
      { id: '2', asset: 'ETH', type: 'momentum', strength: 72, timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString() },
      { id: '3', asset: 'SOL', type: 'reversal', strength: 65, timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString() },
      { id: '4', asset: 'ADA', type: 'trend', strength: 90, timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString() },
      { id: '5', asset: 'DOT', type: 'momentum', strength: 78, timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString() }
    ].slice(0, limit);
  }

  /**
   * 获取热门项目
   */
  async getHotProjects(limit: number = 5): Promise<Project[]> {
    // 直接返回测试数据
    return [
      { id: '1', name: 'Solana', category: 'Layer 1', score: 92, change: 8.5 },
      { id: '2', name: 'Serum', category: 'DEX', score: 88, change: 5.2 },
      { id: '3', name: 'Raydium', category: 'AMM', score: 85, change: 3.7 },
      { id: '4', name: 'Marinade Finance', category: 'Staking', score: 82, change: 2.1 },
      { id: '5', name: 'Star Atlas', category: 'GameFi', score: 79, change: 10.3 }
    ].slice(0, limit);
  }

  /**
   * 获取信号趋势数据
   */
  async getSignalTrendData(days: number = 7): Promise<ChartData[]> {
    // 生成并返回测试数据
    return this.generateTestChartData(days, 'signals');
  }

  /**
   * 获取项目活跃度数据
   */
  async getProjectActivityData(days: number = 7): Promise<ChartData[]> {
    // 生成并返回测试数据
    return this.generateTestChartData(days, 'activity');
  }

  /**
   * 获取订阅计划
   */
  async getSubscriptionPlans(): Promise<SubscriptionPlan[]> {
    // 直接返回测试数据
    return [
      {
        id: '1',
        name: 'Free',
        description: '免费计划，适合新手用户',
        price: 0,
        currency: 'USD',
        billing_cycle: 'monthly',
        features: ['基本信号', '每日限额10次API调用', '邮件通知'],
        api_rate_limit: 10,
        signal_limit: 5
      },
      {
        id: '2',
        name: 'Pro',
        description: '专业计划，适合活跃交易者',
        price: 49.99,
        currency: 'USD',
        billing_cycle: 'monthly',
        features: ['所有信号类型', '无限API调用', '实时通知', '高级分析'],
        api_rate_limit: 1000,
        signal_limit: 100
      },
      {
        id: '3',
        name: 'Enterprise',
        description: '企业计划，适合机构用户',
        price: 299.99,
        currency: 'USD',
        billing_cycle: 'monthly',
        features: ['所有功能', '无限API调用', '专属支持', '自定义集成'],
        api_rate_limit: 10000,
        signal_limit: 1000
      }
    ];
  }

  /**
   * 获取用户订阅
   */
  async getUserSubscriptions(): Promise<Subscription[]> {
    // 直接返回测试数据
    const plans = await this.getSubscriptionPlans();
    return [
      {
        id: '1',
        user_id: 'user123',
        plan_id: '2',
        plan: plans.find(p => p.id === '2') || plans[0],
        status: 'active',
        start_date: new Date(Date.now() - 1000 * 60 * 60 * 24 * 15).toISOString(),
        end_date: new Date(Date.now() + 1000 * 60 * 60 * 24 * 15).toISOString(),
        auto_renew: true,
        current_usage: {
          api_calls: 250,
          signals_generated: 45
        }
      }
    ];
  }

  /**
   * 生成测试图表数据
   */
  private generateTestChartData(days: number, type: 'signals' | 'activity'): ChartData[] {
    const data: ChartData[] = [];
    const today = new Date();

    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);

      const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`;

      if (type === 'signals') {
        data.push({
          date: dateStr,
          signals: Math.floor(Math.random() * 50) + 50,
          activity: 0
        });
      } else {
        data.push({
          date: dateStr,
          signals: 0,
          activity: Math.floor(Math.random() * 30) + 60
        });
      }
    }

    return data;
  }

  /**
   * 获取 DeFi 协议列表
   */
  async getDefiProtocols(): Promise<DefiProtocol[]> {
    // 直接返回测试数据
    return [
      {
        id: '1',
        name: 'Raydium',
        category: 'AMM',
        tvl: 450000000,
        volume_24h: 120000000,
        change_24h: 5.2,
        users: 150000,
        url: 'https://raydium.io',
        twitter: 'https://twitter.com/RaydiumProtocol',
        github: 'https://github.com/raydium-io'
      },
      {
        id: '2',
        name: 'Marinade Finance',
        category: 'Staking',
        tvl: 890000000,
        volume_24h: 25000000,
        change_24h: 2.1,
        users: 200000,
        url: 'https://marinade.finance',
        twitter: 'https://twitter.com/marinadefinance',
        github: 'https://github.com/marinade-finance'
      },
      {
        id: '3',
        name: 'Serum',
        category: 'DEX',
        tvl: 320000000,
        volume_24h: 85000000,
        change_24h: -1.3,
        users: 120000,
        url: 'https://projectserum.com',
        twitter: 'https://twitter.com/projectserum',
        github: 'https://github.com/project-serum'
      },
      {
        id: '4',
        name: 'Jupiter',
        category: 'Aggregator',
        tvl: 150000000,
        volume_24h: 250000000,
        change_24h: 8.7,
        users: 300000,
        url: 'https://jup.ag',
        twitter: 'https://twitter.com/jup_aggregator',
        github: 'https://github.com/jup-ag'
      },
      {
        id: '5',
        name: 'Solana Name Service',
        category: 'DNS',
        tvl: 85000000,
        volume_24h: 5000000,
        change_24h: 1.5,
        users: 500000,
        url: 'https://solana.com',
        twitter: 'https://twitter.com/solananameservice',
        github: 'https://github.com/solana-labs'
      }
    ];
  }

  /**
   * 获取 NFT 市场指标
   */
  async getNftMarketMetrics(): Promise<NftMarketMetrics> {
    // 直接返回测试数据
    return {
      total_collections: 12500,
      total_volume_24h: 45000000,
      average_floor_price: 0.85,
      top_collections: this.getTopNftCollections()
    };
  }

  /**
   * 获取顶级 NFT 集合
   */
  private getTopNftCollections(): NftCollection[] {
    return [
      {
        id: '1',
        name: 'Degenerate Ape Academy',
        category: 'Avatar',
        floor_price: 18.5,
        volume_24h: 12000000,
        volume_7d: 55000000,
        change_24h: 3.2,
        holders: 8500,
        url: 'https://degenerateape.academy',
        twitter: 'https://twitter.com/DegenApeAcademy'
      },
      {
        id: '2',
        name: 'Solana Monkey Business',
        category: 'Avatar',
        floor_price: 22.0,
        volume_24h: 9500000,
        volume_7d: 42000000,
        change_24h: -1.5,
        holders: 7200,
        url: 'https://solanamonkey.business',
        twitter: 'https://twitter.com/SolanaMonkeys'
      },
      {
        id: '3',
        name: 'Okay Bears',
        category: 'Avatar',
        floor_price: 15.2,
        volume_24h: 7800000,
        volume_7d: 35000000,
        change_24h: 2.8,
        holders: 9100,
        url: 'https://okaybears.com',
        twitter: 'https://twitter.com/OkayBearsNFT'
      },
      {
        id: '4',
        name: 'Mad Lads',
        category: 'Avatar',
        floor_price: 8.7,
        volume_24h: 5200000,
        volume_7d: 22000000,
        change_24h: 1.2,
        holders: 12000,
        url: 'https://madlads.io',
        twitter: 'https://twitter.com/MadLadsNFT'
      },
      {
        id: '5',
        name: 'Goblins',
        category: 'Avatar',
        floor_price: 4.5,
        volume_24h: 3100000,
        volume_7d: 14000000,
        change_24h: -0.8,
        holders: 15000,
        url: 'https://goblins.io',
        twitter: 'https://twitter.com/GoblinsNFT'
      }
    ];
  }

  /**
   * 获取NFT市场趋势数据
   */
  async getNftTrendData(days: number = 7): Promise<NftTrendData[]> {
    // 生成并返回测试数据
    return this.generateTestNftTrendData(days);
  }

  /**
   * 生成NFT趋势测试数据
   */
  private generateTestNftTrendData(days: number): NftTrendData[] {
    const data: NftTrendData[] = [];
    const today = new Date();

    // 基础值
    let baseVolume = 30000000;
    let baseFloorPrice = 0.7;

    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);

      const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`;

      // 生成有波动的数据
      const volumeVariation = Math.random() * 20000000 - 10000000;
      const floorPriceVariation = (Math.random() * 0.3 - 0.15);

      data.push({
        date: dateStr,
        volume: Math.max(0, baseVolume + volumeVariation),
        floor_price: Math.max(0, baseFloorPrice + floorPriceVariation)
      });

      // 更新基础值，模拟趋势
      baseVolume += volumeVariation * 0.3;
      baseFloorPrice += floorPriceVariation * 0.2;
    }

    return data;
  }
}

export const localDbService = new LocalDbService();
export default localDbService;
