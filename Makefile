# Makefile for Quantum Minds Eater project

# Compiler
CC = gcc

# Directories
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

# Flags
CFLAGS = -Wall -Wextra -O2

# Source files
SRCS = $(wildcard $(SRC_DIR)/*.c)

# Object files
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# Executable
TARGET = $(BIN_DIR)/quantum_minds_eater

# Default target
all: $(TARGET)

# Build target
$(TARGET): $(OBJS)
	@mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $^

# Build object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c -o $@ $<

# Clean up
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

.PHONY: all clean