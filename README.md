# RabbitMQ

## Routing-Key 命名

|tenant|chain|commodity|action|subject|notes|
|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
|EGamer|eth||filter|tx|新交易,待布隆过滤|
|EGamer|eth||register|tx|已过滤,待登记|
|EGamer|btc||poll_status|tx|进行中交易,待确认|
|EKiller|eos||spawn|address|需要新生成地址|
|EKiller|eos||store|address|需要保存新生成地址|
|EGamer|eth|USDT|withdraw|chain_task|提币任务|
|EGamer|eth|ETH|converge|chain_task|汇聚任务|

### 如下3个exchange
- tenant.chain.action.tx
- tenant.chain.action.address
- tenant.chain.commodity.action.chain_task

## 队列
- filter.tx 交易过滤消息队列
    >  区块链 -> 布隆过滤器 

- EGamer.eth.register 充币交易待记录队列
    > 布隆过滤器 -> 充值记录任务(deposit_registry)

- EGamer.eth.status_poll 待确认状态交易队列
    > 充值记录任务(deposit_registry) -> blockchain

- EGamer.eth.status_update 待更新状态交易队列
    > blockchain -> deposit_registry


