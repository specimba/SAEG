# Unsupported Extra Dataset Cases

This directory contains extra cases that were tested but are not included in `test_extra_dataset.py`.
本目录包含已经测试但未纳入 `test_extra_dataset.py` 的额外样例。

Most cases here are not supported by SAEG, feel free to improve or surpass SAEG!
这里面的大部分测试样例 SAEG 都不支持，请尽情玩耍！

`resource_limited/` contains cases that may not be absolutely unsupported: they exhausted the 12G Docker memory limit or did not finish within the 500s SAEG timeout used for classification. These are separated from ordinary unsupported cases so researchers can retry them with other methods or larger resources.
`resource_limited/` 中的样例并不一定绝对不支持：它们在分类测试中耗尽了 12G Docker 内存上限，或未能在 500s SAEG 超时限制内完成。它们与普通不支持样例分开保存，方便研究者使用其他方法或更高资源重新测试。

## Legend / 图例

- `SIG-ZH`: `libc6_2.23-0ubuntu10_i386.sig`; tested with `libc-2.31-x86.so` and `ld-2.31-x86.so` / 使用 `libc-2.31-x86.so` 和 `ld-2.31-x86.so` 测试。
- `SIG-WD`: `libc6_2.23-0ubuntu7_i386.sig`, `extra.sig`; static list entry / 静态链接条目。
- `SIG-WD-LARGE`: `SIG-WD`; large binary / 大体积二进制。
- `NO-ZT-META`: no `sig` or `libc` specified in the commented ZERATool testset / 注释中的 ZERATool 测试集未指定 `sig` 或 `libc`。
- `NO-ZT-META+LD32`: `NO-ZT-META`; also retested with repo 32-bit libc/ld / 也使用仓库 32-bit libc/ld 重新测试。
- `OOM`: exceeded the Docker memory limit / 超过 Docker 内存上限。
- `TIMEOUT`: did not finish within the classification timeout / 未在分类测试超时限制内完成。
- `NOFLAG`: completed but SAEG did not acquire the flag / 运行结束但 SAEG 未获得 flag。

## Resource-Limited Cases / 资源受限样例

| Path / 路径 | Metadata / 元数据 | Result / 结果 |
| --- | --- | --- |
| `resource_limited/zonghengcup/pwn2` | `SIG-ZH` | `OOM` |
| `resource_limited/wangdingcup2023/bin-3` | `SIG-WD` | `OOM` |
| `resource_limited/wangdingcup2023/bin-7` | `SIG-WD-LARGE` | `TIMEOUT` |
| `resource_limited/wangdingcup2023/bin-9` | `SIG-WD` | `OOM` |

## Unsupported Cases / 暂不支持样例

| Path / 路径 | Metadata / 元数据 | Result / 结果 |
| --- | --- | --- |
| `unsupported_cases/wangdingcup2023/bin-8` | `SIG-WD` | `NOFLAG` |
| `unsupported_cases/zeratool_challenges/demo_bin` | `NO-ZT-META` | `NOFLAG` |
| `unsupported_cases/zeratool_challenges/easy_format` | `NO-ZT-META` | `NOFLAG` |
| `unsupported_cases/zeratool_challenges/hard_format` | `NO-ZT-META` | `NOFLAG` |
| `unsupported_cases/zeratool_challenges/medium_format` | `NO-ZT-META` | `NOFLAG` |
| `unsupported_cases/zeratool_challenges/stack0` | `NO-ZT-META+LD32` | `NOFLAG` |
