#include <bits/stdc++.h>
using namespace std;
int main() {
  int t;
  cin >> t;
  while (t--) {
    long long n, edges, k, d;
    cin >> n >> edges >> k;
    bool cmpGraph = false;
    if (n * (n - 1) / 2 == edges) cmpGraph = true;
    if (cmpGraph) {
      d = 1;
    } else if (edges >= n) {
      d = floor(edges / 2.0);
    } else {
      d = edges;
    }
    if (d == k - 2)
      cout << "YES" << endl;
    else
      cout << "NO" << endl;
  }
  return 0;
}

