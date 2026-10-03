# core/tiny_a5_1.py
# Cài đặt thuật toán TinyA5/1

class TinyA5_1:
    def __init__(self, key_bits):
        if len(key_bits) != 23:
            raise ValueError("Khóa phải có đúng 23 bit!")
        self.key_bits = key_bits[:]
        self.X = key_bits[0:6]
        self.Y = key_bits[6:14]
        self.Z = key_bits[14:23]
        self.step = 0

    def reset(self):
        self.X = self.key_bits[0:6]
        self.Y = self.key_bits[6:14]
        self.Z = self.key_bits[14:23]
        self.step = 0

    def majority(self, a, b, c):
        return 1 if (a + b + c) >= 2 else 0

    def clock_X(self):
        t = self.X[2] ^ self.X[4] ^ self.X[5]
        self.X = [t] + self.X[:-1]

    def clock_Y(self):
        t = self.Y[6] ^ self.Y[7]
        self.Y = [t] + self.Y[:-1]

    def clock_Z(self):
        t = self.Z[2] ^ self.Z[7] ^ self.Z[8]
        self.Z = [t] + self.Z[:-1]

    def generate_bit(self, verbose=False):
        self.step += 1
        x1, y3, z3 = self.X[1], self.Y[3], self.Z[3]
        m = self.majority(x1, y3, z3)
        if verbose:
            print(f"Bước {self.step}: x1={x1} y3={y3} z3={z3} -> m={m}")
        if x1 == m:
            self.clock_X()
            if verbose: print("  Quay X")
        if y3 == m:
            self.clock_Y()
            if verbose: print("  Quay Y")
        if z3 == m:
            self.clock_Z()
            if verbose: print("  Quay Z")
        s = self.X[5] ^ self.Y[7] ^ self.Z[8]
        if verbose:
            print(f"  s = {s}")
        return s

    def encrypt(self, plaintext_bits, verbose=False):
        ciphertext_bits = []
        for p in plaintext_bits:
            s = self.generate_bit(verbose=verbose)
            ciphertext_bits.append(p ^ s)
        return ciphertext_bits

    def decrypt(self, ciphertext_bits, verbose=False):
        self.reset()
        return self.encrypt(ciphertext_bits, verbose=verbose)
