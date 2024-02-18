#include<bits/stdc++.h>
#include<ext/rope>
#include<ext/pb_ds/assoc_container.hpp>
#include<ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;
using namespace __gnu_cxx;
#define ll long long
#define ull unsigned long long
#define bq priority_queue <int,vector<int>,less<int> > //大顶堆
#define sq priority_queue <int,vector<int>,greater<int> > //小顶堆
#define TT int t;cin>>t;while(t--)
typedef pair <int,int> pii;
const int N=3e5+10;
const int mod=1e9+7;
auto max(auto x,auto y){
	return x>y?x:y;
}
auto min(auto x,auto y){
	return x<y?x:y;
}
ll read(){
	ll x=0,y=1;
	char c=getchar();
	while(!isdigit(c)){
		if(c=='-'){
			y=-1;
		}
		c=getchar();
	}
	while(isdigit(c)){
		x=x*10+c-'0';
		c=getchar();
	}
	return x*y;
}
void write(ll x,char c=0)
{
    if(x<0){
    	putchar('-');
    	x=-x;
	}
    char a[20],s=0;
    do{
    	a[++s]=x%10;
    	x=x/10;
	}while(x);
    do{
    	putchar(a[s]+'0');
	}while(--s);
    if(c){
        putchar(c);
    }
}
int prime[N];
bool vis[N];
int cnt=0;

vector <int> a;
void solve(){
    a.clear();
    int n;
    char c;
    cin>>n>>c;
//    cout<<c<<endl;
    char s[N];
    cin>>s+1;
    int cnt1=0;
    for(int i=1;i<=n;i++){
        if(s[i]!=c){
            cnt1++;
        }
        else if(vis[i]){
            a.push_back(i);
        }
    }
    if(cnt1==0){
        cout<<0<<endl;
    }
    else if(s[1]!=c && cnt1==1){
        cout<<1<<endl<<2<<endl;
    }
    else{
       for(int i=0;i<a.size();i++){
//            cout<<a[i]<<endl;
            for(int j=a[i];j<=n;j+=a[i]){
                if(s[j]!=c){
//                    cout<<s[j]<<endl;
                    break;
                }
                if(j+a[i]>n){
                    cout<<1<<endl<<a[i]<<endl;
                    return;
                }
            }

       }
       cout<<2<<endl<<2<<" "<<3<<endl;
    }
}


void Euler_prime(int n)
{
	for(int i=2;i<=n;++i)
	{
		if(!vis[i])
		{prime[cnt++]=i;vis[i]=true;}//vis[i]置为true或不置true都可以
		for(int j=0;j<cnt;++j)
		{
			if(i*prime[j]>n)//判断是否越界
				break;
			vis[i*prime[j]]=true;//筛数
			if(i%prime[j]==0)//时间复杂度为O(n)的关键！
				break;
		}
	}
}
int main(){
    Euler_prime(N);
    TT solve();
	return 0;
}

