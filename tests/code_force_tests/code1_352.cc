/*

    author : s@if

*/

#include<bits/stdc++.h>
#include<ext/pb_ds/assoc_container.hpp>
using namespace __gnu_pbds;
using namespace std;

#define 		NIL 			-1
#define			INF 			1e9
#define         EPS             1e-9
#define         SAIF            main
#define		 	fi	 		    first
#define 		sec 			second
#define 		MAX 			INT_MAX
#define 		ll 			    long long
#define 		PI 			    acos(-1.0)
#define			MOD 			1000000007
#define 		PLL 			pair<ll,ll>
#define 		PII			    pair<int,int>
#define 		ull 			unsigned long long
#define 		For(i,a,b) 		for(int i=a;i<=(int)b;i++)
typedef tree<int, null_type, less<int>, rb_tree_tag,
            tree_order_statistics_node_update> new_data_set;

//*find_by_order(k)  gives the kth element;
//order_of_key(item)   gives the index(number of element strictly less than item) of item;

inline int in() {int x; scanf("%d", &x); return x; }
bool Check(int N , int pos)	{	return (bool) (N & (1<<pos));}
int Set(int N, int pos) {	return N = N | (1<<pos);}

int fx[]={+0,+0,+1,-1,-1,+1,-1,+1};    // King's move
int fy[]={-1,+1,+0,+0,+1,+1,-1,-1};
int hx[]={-2,-2,-1,+1,+2,+2,-1,+1};    // Knight's move
int hy[]={+1,-1,+2,+2,-1,+1,-2,-2};
int dx[]={+1,-1,+0,+0};
int dy[]={+0,+0,+1,-1};

const int MAXN = (int)2e5+9;


void solve(void)
{
    int i,j,k,l,m,n,p,q,x,y,u,v,w,r,tc,t;

    cin>>n; int a[n+9];
    for(i=1; i<=n; i++) cin>>a[i];

    if(n%2==0)
    {
        for(i=1; i<=n; i+=2)
        {
            x = a[i], y = a[i+1];
            cout<<-y<<" "<<x<<" ";
        }
        cout<<endl;
    }
    else{
        if(a[1]+a[2]!=0)
        {
            cout<<-a[3]<<" "<<-a[3]<<" "<<a[1]+a[2]<<" ";
        }
        else if(a[1]+a[3]!=0)
            cout<<-a[2]<<" "<<-a[2]<<" "<<a[1]+a[3]<<" ";
        else
            cout<<-a[1]<<" "<<-a[1]<<" "<<a[3]+a[2]<<" ";

        for(i=4; i<=n; i+=2)
        {
            cout<<-a[i+1]<<" "<<a[i]<<" ";
        }
        cout<<endl;
    }

    return;
}

int SAIF()
{
    int tc = 1, t = 0;

    cin>>tc;

    while(tc--) solve();

    return 0;
}

// read the question correctly (is y a vowel? what are the exact constraints?)
// look out for SPECIAL CASES (n=1?) and overflow (ll vs int?)

