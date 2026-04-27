---
name: issue-handling
description: Use when issues require escalation
user-invocation: false
---

# Issue Handling

在写代码, 做测试, 做任务文档(task.md), 以及各种review工作的时候, 会发现各种问题(issue).
有些问题是写的或被审查的代码或文档本身的bug, 有些问题则是运行环境或前置工作引起的, 后者就需
要agent在竭尽全力执行3种以上不同的解决方案之后, 再自主假设如何处理. 而agent一旦做出假设,
就必须将问题和假设都记录下来, 一方面避免不同的agent重复发现已知问题, 另一方面在完成所有工作
之后, 人类仍然能知道发生了什么事情.

**只按条记录问题, 禁止记录任何其他信息:**
  - "no issue found" - 这类信息没有任何意义, **绝对禁止** - **没有问题就让它空着**
  - "Notes" - 这类信息与真正的问题无关, **绝对禁止**
  - 不知道要写什么就马上住手!

## 读取已知问题

**在进行各项工作的过程中, 必须充分考虑所有已知问题的已有假设(Assumption). 因此:**

  - 编写或review相关内容之前, 要先读brief问题列表.

  - 编写或review相关内容之前, 要先读style问题列表.

  - 编写或review相关内容之前, 要先读env问题列表.


## 记录新问题

- **已经记录的问题禁止重复记录**
- 追加记录新问题的时候要描述清楚问题和所做的假设
- 工作对象(代码, 任务文档, 测试用例等)本身的问题不做记录:
  - 问题可以不做任何假设即自主解决 - 工作对象本身的问题
  - 问题有解决方案 - 工作对象本身的问题


## Brief问题列表


在编写任务文档(task.md)的时候, 需要遵循brief.md文档, 如果文档中有模糊不清或
前后矛盾的地方, 那么agent就必须自己做出合理假设来解决并记录问题.

**注意:**
  - 做任务规划时违反brief.md所引起的问题不是brief问题, 必须马上解决, 禁止记录下来不处理
  - 编写brief.md时发现的brief问题必须马上解决, 禁止记录下来不处理


路径: working/brief-issues.md
记录格式:

```markdown
# Brief Issues

## BI-001: [title]
- **Description**: [Brief ambiguity or contradiction]
- **Assumption**: [what we assume to proceed]
```


## Style问题列表


Style guide issues。如果在此过程中发现模糊不清或前后矛盾的地方, 那么agent就必须自己做出合理假设来解决并记录问题。

**注意:**
  - 工作对象本身的问题不做记录, 必须马上解决


路径: working/style-issues.md
记录格式:

```markdown
# Style Issues

## SI-001: [title]
- **Description**: [Style guide issues]
- **Assumption**: [what we assume to proceed]
```


## Env问题列表


在编译代码和测试的时候, 可能会因为当前运行环境的问题而失败, 必须在探索并执行3种以上不同的解
决方案仍然失败之后, 才可以归类为环境问题记录下来并继续其他工作.

**注意:**
  - 任何代码逻辑问题都绝不属于环境问题, 必须马上解决, 禁止记录下来不处理


路径: working/env-issues.md
记录格式:

```markdown
# Env Issues

## EI-001: [title]
- **Description**: [Environment issues]
- **Assumption**: [what we assume to proceed]
```


<!--
  i18n note: The Chinese text above is optimized for the coding domain and its
  original context. For internationalization, consider extracting the Chinese
  prose into locale-specific message catalogs while keeping the structural
  directives (deduplication rule, 3-attempt rule, per-category format) in the
  template. The category-specific warning blocks are conditionally rendered based
  on issue.name and may also need locale variants.
-->