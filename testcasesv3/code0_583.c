#include <bits/stdc++.h>
using namespace std;
void dbg_out() { cerr << endl; }
template <typename Head, typename... Tail>
void dbg_out(Head H, Tail... T) {
  cerr << ' ' << H;
  dbg_out(T...);
}
pair<int, int> operator*(const pair<int, int> &p, const pair<int, int> &x) {
  pair<int, int> np = make_pair(p.first * x.first, p.second * x.second);
  return np;
}
pair<long long, long long> operator%(const pair<long long, long long> &p,
                                     const pair<long long, long long> &x) {
  pair<long long, long long> np =
      make_pair(p.first % x.first, p.second % x.second);
  return np;
}
pair<long long, long long> operator*(const pair<long long, long long> &p,
                                     const pair<int, int> &x) {
  pair<long long, long long> np =
      make_pair(p.first * x.first, p.second * x.second);
  return np;
}
pair<long long, long long> operator*(const pair<long long, long long> &p,
                                     const pair<long long, long long> &x) {
  pair<long long, long long> np =
      make_pair(p.first * x.first, p.second * x.second);
  return np;
}
pair<long long, long long> operator+(const pair<long long, long long> &p,
                                     const pair<long long, long long> &x) {
  pair<long long, long long> np =
      make_pair(p.first + x.first, p.second + x.second);
  return np;
}
pair<long long, long long> operator-(const pair<long long, long long> &p,
                                     const pair<long long, long long> &x) {
  pair<long long, long long> np =
      make_pair(p.first - x.first, p.second - x.second);
  return np;
}
pair<int, int> operator+(const pair<int, int> &p, const pair<int, int> &x) {
  pair<int, int> np = make_pair(p.first + x.first, p.second + x.second);
  return np;
}
pair<int, int> operator-(const pair<int, int> &p, const pair<int, int> &x) {
  pair<int, int> np = make_pair(p.first - x.first, p.second - x.second);
  return np;
}
vector<int> prime;
bool sortinrev(const pair<int, int> &a, const pair<int, int> &b) {
  return (a.first > b.first);
}
bool sortbysecdesc(const pair<int, int> &a, const pair<int, int> &b) {
  if (a.second == b.second) return a.first > b.first;
  return a.second > b.second;
}
bool sortbysec(const pair<int, int> &a, const pair<int, int> &b) {
  if (a.second == b.second) return a.first > b.first;
  return (a.second < b.second);
}
long long powerm(long long a, long long k) {
  if (!k) {
    return 1;
  }
  long long b = powerm(a, k / 2);
  b = b * b % 998244353;
  if (k % 2) {
    return a * b % 998244353;
  } else {
    return b;
  }
}
long long power(long long a, long long b) {
  if (b == 1) return a;
  if (b == 0) return 1;
  long long m1 = power(a, b / 2);
  if (b % 2) return m1 * m1 * a;
  return m1 * m1;
}
void PFactor(int x) {
  prime.clear();
  for (int i = 2; i <= x / i; i++)
    if (x % i == 0) {
      while (x % i == 0) x /= i, prime.push_back(i);
    }
  if (x > 1) prime.push_back(x);
}
bool isprime(long long a) {
  if (a <= 1) return false;
  if (a == 2 || a == 3) return true;
  if (a % 2 == 0 || a % 3 == 0) return false;
  for (long long i = 5; i * i <= a; i = i + 6) {
    if (a % i == 0 || a % (i + 2) == 0) return false;
  }
  return true;
}
long long read() {
  long long a = 0;
  char b = 1, c;
  do
    if ((c = getchar()) == 45) b = -1;
  while (c < 48 || c > 57);
  do a = (a << 3) + (a << 1) + (c & 15);
  while ((c = getchar()) > 47 && c < 58);
  return a * b;
}
void write(long long x, char c) {
  if (x < 0) putchar(45), x = -x;
  char a[20], s = 0;
  do a[++s] = x % 10 | 48;
  while (x /= 10);
  do putchar(a[s]);
  while (--s);
  putchar(c);
}
const int LOGN = 20;
const int N = (1 << LOGN);
vector<int> g[N];
long long n = 0, m = 0, k = 0;
int a = 0, b = 0, c = 0;
string str;
int d[N] = {0};
int main() {
  int T;
  cin >> T;
  while (T--) {
    cin >> n >> m >> k;
    if (n > m + 1 || m > (n * (n - 1)) / 2) {
      cout << "NO\n";
      continue;
    }
    if (m == n * (n - 1) / 2) {
      if (k >= 3)
        cout << "YES\n";
      else
        cout << "NO\n";
    } else if (k >= 4)
      cout << "YES\n";
    else
      cout << "NO\n";
  }
}

