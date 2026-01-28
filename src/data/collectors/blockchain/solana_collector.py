# Solana Blockchain Data Collector

import time
import json
from datetime import datetime
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.account import Account
from ..base_collector import BaseCollector

class SolanaCollector(BaseCollector):
    """
    Solana 区块链数据采集器
    """

    def __init__(self, config=None):
        """
        初始化 Solana 采集器

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.data_source = "solana"
        self.rpc_url = config.get('rpc_url', 'https://api.mainnet-beta.solana.com')
        self.client = Client(self.rpc_url)
        self.commitment = config.get('commitment', 'confirmed')

    def collect_transactions(self, address, limit=100, **kwargs):
        """
        采集指定地址的交易数据

        Args:
            address: Solana 地址
            limit: 最大交易数
            **kwargs: 其他参数

        Returns:
            采集的交易数据
        """
        try:
            # 获取地址的签名列表
            signatures = self.client.get_signatures_for_address(address, limit=limit, commitment=self.commitment)

            if 'result' not in signatures:
                print(f"Error getting signatures: {signatures}")
                return []

            # 转换数据格式
            transactions = []
            for sig_info in signatures['result']:
                # 获取交易详情
                tx = self.client.get_transaction(sig_info['signature'], commitment=self.commitment)

                if 'result' not in tx:
                    continue

                tx_result = tx['result']

                # 提取交易信息
                transaction_data = {
                    'signature': sig_info['signature'],
                    'slot': sig_info['slot'],
                    'block_time': sig_info.get('blockTime'),
                    'confirmations': sig_info.get('confirmations', 0),
                    'err': sig_info.get('err'),
                    'memo': self._extract_memo(tx_result),
                    'instructions': self._extract_instructions(tx_result),
                    'pre_balances': tx_result.get('meta', {}).get('preBalances', []),
                    'post_balances': tx_result.get('meta', {}).get('postBalances', []),
                    'source': 'solana',
                    'collected_at': datetime.utcnow().isoformat()
                }

                transactions.append(transaction_data)

            # 更新上次采集时间
            self.set_last_collected(datetime.utcnow().isoformat())

            return transactions

        except Exception as e:
            print(f"Error collecting Solana transactions: {str(e)}")
            return []

    def collect_token_holders(self, mint_address, limit=1000, **kwargs):
        """
        采集代币持有者数据

        Args:
            mint_address: 代币 mint 地址
            limit: 最大持有者数
            **kwargs: 其他参数

        Returns:
            采集的持有者数据
        """
        try:
            # 注意：这里需要使用 Solana 的 Token 2022 或 SPL Token 标准
            # 实际实现可能需要使用第三方 API 或索引器，因为直接从链上获取所有持有者比较复杂

            # 这里使用一个模拟实现，实际项目中需要根据具体情况调整
            holders = []

            # 模拟数据，实际项目中需要替换为真实数据获取逻辑
            for i in range(min(10, limit)):
                holders.append({
                    'address': f"HolderAddress{i}",
                    'amount': 1000000000 + i * 100000000,
                    'percentage': (1000000000 + i * 100000000) / 100000000000,
                    'source': 'solana',
                    'collected_at': datetime.utcnow().isoformat()
                })

            # 更新上次采集时间
            self.set_last_collected(datetime.utcnow().isoformat())

            return holders

        except Exception as e:
            print(f"Error collecting token holders: {str(e)}")
            return []

    def collect_nft_metadata(self, mint_address, **kwargs):
        """
        采集 NFT 元数据

        Args:
            mint_address: NFT mint 地址
            **kwargs: 其他参数

        Returns:
            采集的 NFT 元数据
        """
        try:
            # 获取 NFT 元数据
            # 实际实现需要根据具体的 NFT 标准（如 Metaplex）来获取

            # 模拟数据，实际项目中需要替换为真实数据获取逻辑
            nft_metadata = {
                'mint_address': mint_address,
                'name': "Test NFT",
                'symbol': "TEST",
                'uri': "https://example.com/metadata.json",
                'seller_fee_basis_points': 500,
                'creators': [
                    {
                        'address': "CreatorAddress1",
                        'verified': True,
                        'share': 100
                    }
                ],
                'source': 'solana',
                'collected_at': datetime.utcnow().isoformat()
            }

            # 更新上次采集时间
            self.set_last_collected(datetime.utcnow().isoformat())

            return nft_metadata

        except Exception as e:
            print(f"Error collecting NFT metadata: {str(e)}")
            return {}

    def collect_program_accounts(self, program_id, limit=100, **kwargs):
        """
        采集程序账户数据

        Args:
            program_id: 程序 ID
            limit: 最大账户数
            **kwargs: 其他参数

        Returns:
            采集的程序账户数据
        """
        try:
            # 获取程序账户
            accounts = self.client.get_program_accounts(program_id, commitment=self.commitment)

            if 'result' not in accounts:
                print(f"Error getting program accounts: {accounts}")
                return []

            # 转换数据格式
            program_accounts = []
            for acc in accounts['result'][:limit]:
                account_data = {
                    'pubkey': acc['pubkey'],
                    'lamports': acc['account']['lamports'],
                    'owner': acc['account']['owner'],
                    'executable': acc['account']['executable'],
                    'rent_epoch': acc['account']['rentEpoch'],
                    'data_length': len(acc['account']['data'][0]) if acc['account']['data'] else 0,
                    'source': 'solana',
                    'collected_at': datetime.utcnow().isoformat()
                }

                program_accounts.append(account_data)

            # 更新上次采集时间
            self.set_last_collected(datetime.utcnow().isoformat())

            return program_accounts

        except Exception as e:
            print(f"Error collecting program accounts: {str(e)}")
            return []

    def _extract_memo(self, tx_result):
        """
        从交易结果中提取 memo

        Args:
            tx_result: 交易结果

        Returns:
            memo 内容
        """
        try:
            instructions = tx_result.get('transaction', {}).get('message', {}).get('instructions', [])

            for instr in instructions:
                if 'parsed' in instr and instr['parsed']['type'] == 'memo':
                    return instr['parsed']['info']['memo']

            return None
        except:
            return None

    def _extract_instructions(self, tx_result):
        """
        从交易结果中提取指令

        Args:
            tx_result: 交易结果

        Returns:
            指令列表
        """
        try:
            instructions = tx_result.get('transaction', {}).get('message', {}).get('instructions', [])
            return instructions
        except:
            return []

    def collect(self, **kwargs):
        """
        通用采集方法

        Args:
            **kwargs: 采集参数

        Returns:
            采集的数据
        """
        # 根据参数决定采集类型
        if 'address' in kwargs:
            return self.collect_transactions(kwargs['address'], **kwargs)
        elif 'mint_address' in kwargs:
            return self.collect_token_holders(kwargs['mint_address'], **kwargs)
        elif 'program_id' in kwargs:
            return self.collect_program_accounts(kwargs['program_id'], **kwargs)
        else:
            print("No valid collection type specified")
            return []
