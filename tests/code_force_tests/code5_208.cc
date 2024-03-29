#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;

#define      ll                  long long
#define      pb                 push_back
#define      mp                 make_pair
#define      all(x)             x.begin(),x.end()
#define      Ceil(x,y)           ((x+y-1)/y)
#define      gcd(a,b)            __gcd(a,b)
#define      lcm(a,b)           (a*b)/gcd(a,b)
#define      InTheNameOfGod      ios::sync_with_stdio(0);cin.tie(0); cout.tie(0);

template <typename T>
using ordered_set = tree<T, null_type, less_equal<T>, rb_tree_tag, tree_order_statistics_node_update>;

constexpr ll mod = 1e9 + 7;
const ll N=3e6+5;

void solve(){
   ll n,k,sum=0;
   cin>>n>>k;
   vector<ll> a(n);
   for(ll i=0;i<n;i++){
      cin>>a[i];
      sum+=a[i];
   }
   if(sum<=k){
      cout<<0<<endl;
      return;
   }
   sum=0;
   sort(all(a));
   if(n==1){
      ll ans= max(0LL,a[0]-k);
      cout<<ans<<endl;
      return;
   }
   ll ans=1e18;
   ll baki=n-1,cur;
   for(ll i=1;i<n;i++){
      sum+=a[i];
      if(sum>k){
         ll bal = Ceil(sum-k,baki);
         cur=baki-1;
         cur+=a[0]+abs(bal);
      }
      else{
         ll bal= (k-sum)/baki;
         cur=baki-1;
         cur+=max(0LL,a[0]-bal);
      }
      ans=min(ans,cur);

      baki--;

   }

   cout<<ans<<endl;
   
}

int main(){
   InTheNameOfGod;
   ll Test=1;
   cin>>Test;
   while(Test--){
     solve();
    }
  return 0;
}

