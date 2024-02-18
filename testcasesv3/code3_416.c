#include <bits/stdc++.h>
using namespace std;
int main() {
  ios_base::sync_with_stdio(false), cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, a, b;
    cin >> n >> a >> b;
    if (abs(a - b) > 1 || a + b + 2 > n)
      cout << -1 << '\n';
    else {
      vector<int> ans(n);
      iota(ans.begin(), ans.end(), 1);
      int i = a > b ? 1 : 0;
      int x = max(a, b);
      while (x--) {
        swap(ans[i], ans[i + 1]);
        i += 2;
      }
      if (a == b) swap(ans[i], ans[i + 1]);
      for (auto &i : ans) {
        cout << i << " ";
      }
      cout << '\n';
    }
  }
  return 0;
}

