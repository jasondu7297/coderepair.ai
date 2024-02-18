#include <bits/stdc++.h>
using namespace std;
vector<long long> sieve(long long n) {
  long long* arr = new long long[n + 1]();
  vector<long long> vect;
  for (long long i = 2; i <= n; i++)
    if (arr[i] == 0) {
      vect.push_back(i);
      for (long long j = 2 * i; j <= n; j += i) arr[j] = 1;
    }
  return vect;
}
long long expo(long long a, long long b, long long MOD) {
  long long res = 1;
  while (b > 0) {
    if (b & 1) res = (res * a) % MOD;
    a = (a * a) % MOD;
    b = b >> 1;
  }
  return res;
}
long long gcd(long long a, long long b) {
  if (a == 0) return b;
  return gcd(b % a, a);
}
long long findGCD(long long arr[], long long n) {
  long long result = arr[0];
  for (long long i = 1; i < n; i++) {
    result = gcd(arr[i], result);
    if (result == 1) {
      return 1;
    }
  }
  return result;
}
string decToBinary(long long n) {
  string output = "";
  while (n) {
    if (n & 1) {
      output = '1' + output;
    } else {
      output = '0' + output;
    }
    n >>= 1;
  }
  return output;
}
long long isSubstring(string s1, string s2) {
  long long M = s1.length();
  long long N = s2.length();
  for (long long i = 0; i <= N - M; i++) {
    long long j;
    for (j = 0; j < M; j++)
      if (s2[i + j] != s1[j]) break;
    if (j == M) return i;
  }
  return -1;
}
void solve() {
  long long n, k;
  cin >> n >> k;
  vector<long long> v(n);
  for (long long i = 0; i < n; i++) {
    cin >> v[i];
  }
  sort(v.begin(), v.end());
  vector<long long> sums(n);
  sums[0] = v[0];
  for (long long i = 1; i < n; i++) {
    sums[i] = sums[i - 1] + v[i];
  }
  long long min = 2e5 + 1;
  for (long long i = 0; i < n; i++) {
    long long x;
    if ((v[0] + k - sums[n - i - 1]) < 0 &&
        abs((v[0] + k - sums[n - i - 1])) % (i + 1)) {
      x = v[0] - ((v[0] + k - sums[n - i - 1]) / (i + 1)) + 1;
    } else {
      x = v[0] - ((v[0] + k - sums[n - i - 1]) / (i + 1));
    }
    if (x >= 0) {
      if (x + i < min) {
        min = x + i;
      }
    }
  }
  if (min > 2e5) {
    cout << 0 << endl;
  } else {
    cout << min << endl;
  }
}
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  ;
  long long t;
  cin >> t;
  while (t--) {
    solve();
  }
}

