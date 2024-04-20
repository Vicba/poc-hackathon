// ethereum.js
import Web3 from 'web3';
var web3 = new Web3(window.ethereum);


async function enableEthereum() {
    if (window.ethereum) {
      try {
        await window.ethereum.enable();
        console.log('Ethereum enabled');
      } catch (error) {
        console.error('User denied account access');
      }
    } else {
      console.error('No Ethereum provider detected');
    }
  }

  async function sendTransaction(method, contract, senderAddress, ...args) {
    // Assign the global Ethereum provider object to a variable
    const ethereum = window.ethereum;
  
    // Call the enableEthereum function to request user permissions
    await enableEthereum();
  
    const encodedABI = method.encodeABI();
    const estimatedGas = await method.estimateGas({ from: senderAddress });
    const gas = Math.round(Number(estimatedGas) * 1.1);
  
    const transactionParameters = {
      from: senderAddress,
      to: contract.options.address,
      data: encodedABI,
      gas: Web3.utils.toHex(gas),
    };
  
    const txHash = await ethereum.request({
      method: 'eth_sendTransaction',
      params: [transactionParameters],
    });
  
    let receipt = await getConfirmation(txHash)
    while(receipt == null) {
      receipt = await getConfirmation(txHash)
    }
    console.log(receipt)
    return txHash;
  }

  async function getConfirmation(txHash) {
    let receipt = null
    try {
      receipt = await web3.eth.getTransactionReceipt(txHash);
    } catch {
      
    }
    return receipt
  }
  
export { sendTransaction };
