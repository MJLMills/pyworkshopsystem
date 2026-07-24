# MicroPython & RP2040 Execution Rules

## Context
- This package runs on an RP2040 microcontroller using MicroPython.
- Resource constraints are high: Max 264KB RAM, limited flash storage.

## Code Optimization Principles
- Never use standard heavy Python modules. Use micro-variants (e.g., `ujson` instead of `json`, `utime` instead of `time`).
- Minimize heap allocations. Avoid generating string fragments or list objects inside loops.
- Use generator expressions instead of list comprehensions when processing arrays to conserve RAM.
- Prefer global static buffers or bytearrays over continuous object creation to avoid garbage collection spikes.
- Use explicit integer math or bitwise shift operations (`<<`, `>>`) instead of float operations where possible.
- Avoid deep object-oriented inheritance structures; use simple flat classes or lightweight function lookups.
- Optimization of hardware interaction is much more important than optimization of startup time.

## Decorators & Language Tools
- Prioritize the `@micropython.native` decorator for code blocks requiring faster execution speeds.
- Prioritize the `@micropython.viper` decorator for ultra-high-speed byte/integer array logic or direct memory operations.
- Always use explicit integer type hints inside viper functions (e.g., `x: int`).

## Module References
- Hardware abstraction must strictly use the `machine` module (e.g., `machine.Pin`, `machine.I2C`).
- Do not use desktop testing libraries inside package code files.

# MicroPython ADC Optimization Rules
- Pre-allocate a `bytearray` or `array('H')` before starting continuous ADC reads.
- Never allocate memory inside loops, timer callbacks, or Interrupt Service Routines (ISRs).
- Use `micropython.viper` or `micropython.native` decorators for high-speed sampling loops.
- Implement efficient bitwise shifting over math modules for multi-sample averaging.
- Use `machine.mem32` direct register access if Copilot needs to change hardware clock dividers.
- Always use `try/finally` blocks to ensure peripheral pins or timers are released properly on error.
- Use `const()` for pin mappings, oversampling rates, and calibration constants.