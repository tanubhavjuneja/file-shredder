#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/statvfs.h>
#include <errno.h>
#include <time.h>
#include <openssl/evp.h>

// ---------- Logging ----------
#define LOG(fmt, ...) fprintf(stdout, "[*] " fmt "\n", ##__VA_ARGS__)
#define ERR(fmt, ...) fprintf(stderr, "[!] " fmt " (errno=%d: %s)\n", ##__VA_ARGS__, errno, strerror(errno))

// ---------- Encryption ----------
int encrypt_chunk(unsigned char *data, size_t len, unsigned char *out, unsigned char *key, unsigned char *iv) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) return -1;

    int outlen1, outlen2;
    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv) != 1) return -1;

    if (EVP_EncryptUpdate(ctx, out, &outlen1, data, (int)len) != 1) return -1;
    if (EVP_EncryptFinal_ex(ctx, out + outlen1, &outlen2) != 1) return -1;

    EVP_CIPHER_CTX_free(ctx);
    return outlen1 + outlen2;
}

// ---------- Disk Wiper ----------
void wipe_free_space(const char *path, int passes, size_t chunk_size) {
    struct statvfs fs;
    if (statvfs(path, &fs) != 0) {
        ERR("statvfs failed");
        return;
    }

    unsigned long long free_space = fs.f_bsize * fs.f_bavail;
    LOG("Detected free space: %llu MB", free_space / (1024 * 1024));

    for (int p = 0; p < passes; p++) {
        LOG("=== Pass %d/%d ===", p + 1, passes);

        const char *patterns[] = {"zeros", "ones", "random", "encrypted"};
        for (int pat = 0; pat < 4; pat++) {
            char filename[256];
            snprintf(filename, sizeof(filename), "%s/shred_temp_%d_%d.dat", path, p, pat);

            LOG("Writing pattern: %s -> %s", patterns[pat], filename);

            int fd = open(filename, O_CREAT | O_WRONLY | O_TRUNC, 0600);
            if (fd < 0) {
                ERR("Failed to open temp file");
                continue;
            }

            unsigned char *buf = malloc(chunk_size);
            unsigned char *outbuf = malloc(chunk_size + 32);
            if (!buf || !outbuf) {
                ERR("Memory allocation failed");
                close(fd);
                free(buf);
                free(outbuf);
                continue;
            }

            size_t written = 0;
            while (1) {
                if (strcmp(patterns[pat], "zeros") == 0) {
                    memset(buf, 0x00, chunk_size);
                } else if (strcmp(patterns[pat], "ones") == 0) {
                    memset(buf, 0xFF, chunk_size);
                } else if (strcmp(patterns[pat], "random") == 0) {
                    for (size_t i = 0; i < chunk_size; i++) buf[i] = rand() % 256;
                } else if (strcmp(patterns[pat], "encrypted") == 0) {
                    for (size_t i = 0; i < chunk_size; i++) buf[i] = rand() % 256;
                    unsigned char key[32], iv[16];
                    for (int i = 0; i < 32; i++) key[i] = rand() % 256;
                    for (int i = 0; i < 16; i++) iv[i] = rand() % 256;
                    int enc_size = encrypt_chunk(buf, chunk_size, outbuf, key, iv);
                    if (enc_size > 0) memcpy(buf, outbuf, enc_size);
                }

                ssize_t w = write(fd, buf, chunk_size);
                if (w <= 0) {
                    break; // likely disk full
                }
                written += w;
            }

            LOG("Wrote %zu MB", written / (1024 * 1024));

            close(fd);
            free(buf);
            free(outbuf);

            // Delete temp file
            if (remove(filename) != 0) {
                ERR("Failed to remove temp file");
            } else {
                LOG("Removed %s", filename);
            }
        }
    }

    LOG("✅ Free space wipe complete.");
}

// ---------- Main ----------
int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <path> [passes]\n", argv[0]);
        printf("Example (Linux):   sudo %s / 3\n", argv[0]);
        printf("Example (Windows): %s C:/ 3\n", argv[0]);
        return 1;
    }

    const char *path = argv[1];
    int passes = (argc > 2) ? atoi(argv[2]) : 3;
    size_t chunk_size = 512 * 1024 * 1024; // 512MB

    srand((unsigned int)time(NULL));
    wipe_free_space(path, passes, chunk_size);
    return 0;
}
