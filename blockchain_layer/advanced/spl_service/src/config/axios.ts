import axios, { AxiosRequestConfig } from 'axios';
import { MASTER_PUBLIC_KEY, NETWORK_LOCAL } from './settings';


// Define the request parameters
export const requestConfig: AxiosRequestConfig = {
    method: 'post',
    url: NETWORK_LOCAL,
    headers: {
      'Content-Type': 'application/json',
    },
    data: {
      jsonrpc: '2.0',
      id: 1,
      method: 'getProgramAccounts',
      params: [
        'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA',
        {
          encoding: 'jsonParsed',
          filters: [
            {
              dataSize: 165,
            },
            {
              memcmp: {
                offset: 32,
                bytes: MASTER_PUBLIC_KEY,
              },
            },
          ],
        },
      ],
    },
  };