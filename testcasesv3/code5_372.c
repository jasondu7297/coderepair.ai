#include <bits/stdc++.h>
using namespace std;
int main(void) {
  long long t, n, k, a[200000], ans, sum;
  cin >> t;
  while (t--) {
    cin >> n >> k;
    ans = sum = 0;
    for (int i = (0); i < (n); i++) {
      cin >> a[i];
      sum += a[i];
    }
    if (sum <= k) {
      cout << 0 << endl;
      continue;
    } else if (n == 1) {
      cout << a[0] - k << endl;
      continue;
    }
    sort(a, a + n);
    for (int i = n - 1; i && sum > k; i--)
      if (a[i] - a[0] >= n - i)
        ans++, sum -= a[i] - a[0];
      else {
        int ad = (sum - k - 1) / (n - i) + 1;
        if (a[i] - a[0] + ad > n - i) {
          int de = a[i] - a[0] - n + i;
          ans += de + 1;
          a[0] -= de;
          sum -= de * (n - i) + a[i] - a[0];
        } else {
          ans += ad;
          break;
        }
      }
    cout << ans << endl;
  }
  return 0;
}

