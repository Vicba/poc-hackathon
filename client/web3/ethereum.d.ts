import { Contract } from 'web3-eth-contract';
import { AccountStore } from '@/store/account';

declare function sendTransaction(
  method: any,
  contract: Contract,
  accountStore: string,
): Promise<string>;

export { sendTransaction };