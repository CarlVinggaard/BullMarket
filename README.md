### user/{userId}
- name: string
- cash: double
- portfolio: object[]
  - stockCode: string
  - quantity: integer
- trades: object[]
  - stockCode: string
  - type: string ('buy' | 'sell')
  - quantity: integer
  - price: double
  - timestamp: timestamp
- valueAtLastTrade: double

### stocks/{stockId}
- stockCode: string
- description: string

### comments/{commentId}
- stockId: string
- content: string
- userId: string
- userName: string
- createdAt: timestamp