#include <bits/stdc++.h>
using namespace std;
int t, n, a[100005], b[100005], wz[100005];
const long long INF = 1e9;
long long sum;
int jdz(int x) {
  if (x < 0) return -x;
  return x;
}
bool cmp(int x, int y) { return jdz(a[x]) < jdz(a[y]); }
int main() {
  scanf("%d", &t);
  while (t--) {
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
      wz[i] = i;
      scanf("%d", &a[i]);
    }
    sort(wz + 1, wz + n + 1, cmp);
    if (n & 1) {
      b[wz[1]] = a[wz[2]] + a[wz[3]];
      b[wz[2]] = -a[wz[1]];
      b[wz[3]] = -a[wz[1]];
      for (int i = 4; i <= n; i += 2) {
        if (jdz(a[wz[i]]) == jdz(a[wz[i + 1]])) {
          if (a[wz[i]] == a[wz[i + 1]]) {
            b[wz[i]] = 1;
            b[wz[i + 1]] = -1;
          } else {
            b[wz[i]] = 1;
            b[wz[i + 1]] = 1;
          }
        } else {
          b[wz[i]] = -a[wz[i + 1]];
          b[wz[i + 1]] = a[wz[i]];
        }
      }
      sum = 0;
      for (int i = 1; i <= n; i++) {
        sum = sum + jdz(b[i]);
      }
      if (sum > INF) {
        for (int i = 5; i < n; i += 2) {
          if (jdz(a[wz[i]]) == jdz(a[wz[i + 1]])) {
            if (a[wz[i]] == a[wz[i + 1]]) {
              b[wz[i]] = 1;
              b[wz[i + 1]] = -1;
            } else {
              b[wz[i]] = 1;
              b[wz[i + 1]] = 1;
            }
          } else {
            b[wz[i]] = -a[wz[i + 1]];
            b[wz[i + 1]] = a[wz[i]];
          }
        }
        if (jdz(a[wz[4]]) == jdz(a[wz[n]])) {
          if (a[wz[4]] == a[wz[n]]) {
            b[wz[4]] = 1;
            b[wz[n]] = -1;
          } else {
            b[wz[4]] = 1;
            b[wz[n]] = 1;
          }
        } else {
          b[wz[4]] = -a[wz[n]];
          b[wz[n]] = a[wz[4]];
        }
      }
      for (int i = 1; i <= n; i++) printf("%d ", b[i]);
    } else {
      for (int i = 1; i <= n; i += 2) {
        printf("%d %d ", -a[i + 1], a[i]);
      }
    }
    printf("\n");
  }
  return 0;
}

