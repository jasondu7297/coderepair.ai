#include <bits/stdc++.h>
#pragma GCC target("avx2")
#pragma GCC optimize("179")
#pragma GCC optimize("unroll-loops")
using namespace std;
void solve() {
  long long n, s = 0, ind = -1;
  cin >> n;
  vector<long long> a(n);
  for (long long i = 0; i < n; ++i) {
    cin >> a[i];
    s += a[i];
  }
  if (n < 10) {
    cout << -(s - a[0]) << " ";
    for (long long i = 1; i < n; ++i) {
      cout << a[0] << " ";
    }
    cout << '\n';
    return;
  }
  if (n % 2 == 0) {
    for (long long i = 0; i < n; i += 2) {
      cout << -a[i + 1] << " " << a[i] << '\n';
    }
    return;
  }
  for (long long i = 0; i < n; ++i) {
    if (s >= 0 && a[i] >= 0) {
      ind = i;
      break;
    }
    if (s < 0 && a[i] < 0) {
      ind = i;
      break;
    }
  }
  if (s == a[ind]) {
    for (long long i = 0; i < n; ++i) {
      if (s != a[i]) {
        ind = i;
        break;
      }
    }
  }
  for (long long i = 0; i < n; ++i) {
    if (i != ind)
      cout << a[ind] << ' ';
    else
      cout << -(s - a[ind]) << " ";
  }
  cout << '\n';
}
signed main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr), cout.tie(nullptr);
  long long t;
  cin >> t;
  while (t--) {
    solve();
  }
}

