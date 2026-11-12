---
name: joyally-midway
description: 开发、排障和验证基于装饰器与依赖注入的 Midway Web 服务。用于常驻 Node.js 应用的 Controller、Service、配置、Middleware、生命周期、异常、数据访问和 HTTP 测试；不用于 Serverless/FaaS 函数开发或部署。
---

# Joyally Midway

处理现有 Midway Web 应用时，以仓库实际安装的版本、Web 适配器和项目约定为准。先读项目 `AGENTS.md`、`package.json` 与锁文件、`src/configuration.ts`、环境配置、相关 Controller/Service/Middleware 和现有测试。不要因为文档首页展示新版本，就迁移已有应用的装饰器、组件或启动方式。

## 确定请求与依赖链

1. 从 HTTP 方法和路由定位 Controller、参数来源、响应中间件、调用方契约与受影响的 Service。Controller 负责 HTTP 输入输出；业务判断和外部调用沿项目现有边界放在 Service 或纯函数中。
2. 核对 `@Configuration` 导入的 Web 适配器与组件。Egg、Koa 和 Express 的 `Application`、`Context` 以及底层行为不能混用；只使用仓库已安装版本支持的 API。
3. `@Provide()` 暴露 Service，`@Inject()` 注入依赖；由容器创建依赖链中的对象。使用类类型注入时保留运行时 value import，检查 decorator metadata 和循环依赖。直接 `new` Service 的单测不能证明容器注入成功。
4. 默认请求作用域与单例对象要分清。Middleware 是单例，不要在其中长期持有依赖请求 `ctx` 的 Service；需要该服务时在当前请求的 `ctx.requestContext` 中解析。全局定时器、后台任务和生命周期回调也要核对自己的容器和上下文。

## 保持 Web 行为可解释

- 参数取值、类型转换和校验以当前版本的装饰器和现有 API 契约为准；不要假定 TypeScript 类型本身会验证运行时输入。检查缺失字段、重复 Query、上传和边界值时，使用实际 Web 适配器的行为。
- Middleware 遵循 `await next()` 的执行顺序。改动全局注册顺序、`match`/`ignore`、统一响应或错误处理时，核对完整路由链；原始响应协议只做精确路径排除，不扩大到整组 API。
- `@Catch` 或统一响应层接管异常后，确认服务端仍记录未知错误及其 cause/stack，客户端只收到稳定且脱敏的状态与消息。区分业务失败、HTTP 状态和框架异常。
- 配置先核对 `config.default.*` 与当前环境文件的合并结果，再看 `@Config`、运行时变量及注入时机。不要在 constructor 中假定配置注入已完成；秘密值保留在项目既有注入链中。
- `onReady` 用于容器就绪后的初始化；依赖已启动服务的动作放在 `onServerReady`；启动的资源在 `onStop` 清理。说明健康检查究竟证明主服务存活还是依赖就绪。
- 数据源、ORM 与外部客户端沿用项目已配置的组件和版本；不能把实体定义、连接成功或单测当成数据库迁移已执行的证据。

## 验证与排障

先跑相关 Service 的最窄测试，再用项目测试入口启动真实 Midway App，发起 HTTP 请求验证路由、参数、Middleware、异常与完整 DI 链，并在结束时关闭 App。对配置、生命周期、数据源或启动行为的改动，按项目门禁继续验证对应环境和构建；分别报告源码测试、构建、启动及外部依赖的证据。

排障按实际发生顺序定位：配置加载 → 组件导入 → 容器解析 → 生命周期 → Web 路由和 Middleware → 外部依赖。先读完整错误栈和已安装包版本，再查对应文档；不要把一个 mock 或直接构造对象的通过结果外推为 HTTP 链路正常。

按问题查阅 [Web 开发参考](references/web-development.md)。本技能聚焦常驻 Web 服务；函数触发器、FC、FaaS 构建发布和 Serverless Context 不在此范围。
