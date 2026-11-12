# Midway Web 开发参考

这份参考按问题查阅，不是安装指令。官方站点的当前版本与项目锁定版本可能不同；先核对 `@midwayjs/core`、Web 适配器及组件版本，再选择对应版本文档。以下链接指向公开的 Midway 3.x 文档；若项目使用其他版本，在同一官方文档站切换版本后再采用代码示例。

| 当前问题 | 核对点 | 官方文档 |
| --- | --- | --- |
| 路由或参数 | HTTP 方法、Controller 前缀、Query/Body/Param、实际 Context | [路由和控制器](https://midwayjs.org/docs/3.0.0/controller)、[Application 和 Context](https://midwayjs.org/docs/3.0.0/req_res_app) |
| Service 无法注入 | `@Provide`、`@Inject`、value import、容器解析、作用域 | [服务和注入](https://midwayjs.org/docs/3.0.0/service)、[依赖注入](https://midwayjs.org/docs/3.0.0/container) |
| Middleware 行为异常 | 注册顺序、`await next()`、`match`/`ignore`、请求作用域解析 | [Web 中间件](https://midwayjs.org/docs/3.0.0/middleware)、[Web 路由表](https://midwayjs.org/docs/3.0.0/router_table) |
| 鉴权和输入校验 | 适用 Guard、Pipe 或项目既有校验组件；确认错误状态 | [守卫](https://midwayjs.org/docs/3.0.0/guard)、[管道](https://midwayjs.org/docs/3.0.0/pipe)、[参数校验](https://midwayjs.org/docs/3.0.0/extensions/validate) |
| 异常未记录或响应泄漏 | Filter 匹配、异常日志、客户端错误形状 | [异常处理](https://midwayjs.org/docs/3.0.0/error_filter)、[自定义错误](https://midwayjs.org/docs/3.0.0/custom_error) |
| 环境差异或启动失败 | 默认与环境配置合并、环境值、启动阶段与退出清理 | [多环境配置](https://midwayjs.org/docs/3.0.0/env_config)、[运行环境](https://midwayjs.org/docs/3.0.0/environment)、[生命周期](https://midwayjs.org/docs/3.0.0/lifecycle) |
| 日志与调试 | 上下文日志、错误栈、实际启动入口 | [日志](https://midwayjs.org/docs/3.0.0/logger_v3)、[调试](https://midwayjs.org/docs/3.0.0/debugger) |
| 数据访问 | 已启用的数据源、实体绑定、连接与迁移边界 | [数据源管理](https://midwayjs.org/docs/3.0.0/data_source)、[Sequelize](https://midwayjs.org/docs/3.0.0/extensions/sequelize) |
| 验证真实链路 | `createApp`、`createHttpRequest`、`close`、测试隔离与 Mock 边界 | [测试](https://midwayjs.org/docs/3.0.0/testing)、[数据模拟](https://midwayjs.org/docs/3.0.0/mock) |

只有当前变更确实涉及组件扩展、AOP、重试或 ESM 时，再查对应的 [组件](https://midwayjs.org/docs/3.0.0/midway_component)、[拦截器](https://midwayjs.org/docs/3.0.0/aspect)、[重试](https://midwayjs.org/docs/3.0.0/retry) 或 [ESModule](https://midwayjs.org/docs/3.0.0/esm) 文档。重试外部写入前，必须核对调用方是否具备幂等或读回机制。
