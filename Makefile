CC ?= cc
CLANG ?= clang
CFLAGS := -std=c11 -Wall -Wextra -Werror -Iinclude
BUILD := build
SRCS := src/aster.c src/platform.c

.PHONY: all clean check-x86_64 check-aarch64 check-riscv64 check-all
all: check-x86_64

$(BUILD):
	mkdir -p $(BUILD)

check-x86_64: | $(BUILD)
	$(CC) $(CFLAGS) -c src/aster.c -o $(BUILD)/aster-x86_64.o
	$(CC) $(CFLAGS) -c src/platform.c -o $(BUILD)/platform-x86_64.o

check-aarch64: | $(BUILD)
	$(CLANG) -target aarch64-none-elf -ffreestanding $(CFLAGS) -c src/aster.c -o $(BUILD)/aster-aarch64.o
	$(CLANG) -target aarch64-none-elf -ffreestanding $(CFLAGS) -c src/platform.c -o $(BUILD)/platform-aarch64.o

check-riscv64: | $(BUILD)
	$(CLANG) -target riscv64-none-elf -ffreestanding $(CFLAGS) -c src/aster.c -o $(BUILD)/aster-riscv64.o
	$(CLANG) -target riscv64-none-elf -ffreestanding $(CFLAGS) -c src/platform.c -o $(BUILD)/platform-riscv64.o

check-all: check-x86_64 check-aarch64 check-riscv64

clean:
	rm -rf $(BUILD)
