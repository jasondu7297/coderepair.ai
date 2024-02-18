#include<bits/stdc++.h>
using namespace std;
#define int long long int
int parent[100];
int findpar(int x)
{
    if(x==parent[x])
    {
        return x;
    }
    return parent[x]=findpar(parent[x]);
}
void merge(int array[], int const left, int const mid, int const right)
{
    auto const subArrayOne = mid - left + 1;
    auto const subArrayTwo = right - mid;
  
    // Create temp arrays
    auto *leftArray = new int[subArrayOne],
         *rightArray = new int[subArrayTwo];
  
    // Copy data to temp arrays leftArray[] and rightArray[]
    for (auto i = 0; i < subArrayOne; i++)
        leftArray[i] = array[left + i];
    for (auto j = 0; j < subArrayTwo; j++)
        rightArray[j] = array[mid + 1 + j];
  
    auto indexOfSubArrayOne = 0, // Initial index of first sub-array
        indexOfSubArrayTwo = 0; // Initial index of second sub-array
    int indexOfMergedArray = left; // Initial index of merged array
  
    // Merge the temp arrays back into array[left..right]
    while (indexOfSubArrayOne < subArrayOne && indexOfSubArrayTwo < subArrayTwo) {
        if (leftArray[indexOfSubArrayOne] <= rightArray[indexOfSubArrayTwo]) {
            array[indexOfMergedArray] = leftArray[indexOfSubArrayOne];
            indexOfSubArrayOne++;
        }
        else {
            array[indexOfMergedArray] = rightArray[indexOfSubArrayTwo];
            indexOfSubArrayTwo++;
        }
        indexOfMergedArray++;
    }
    // Copy the remaining elements of
    // left[], if there are any
    while (indexOfSubArrayOne < subArrayOne) {
        array[indexOfMergedArray] = leftArray[indexOfSubArrayOne];
        indexOfSubArrayOne++;
        indexOfMergedArray++;
    }
    // Copy the remaining elements of
    // right[], if there are any
    while (indexOfSubArrayTwo < subArrayTwo) {
        array[indexOfMergedArray] = rightArray[indexOfSubArrayTwo];
        indexOfSubArrayTwo++;
        indexOfMergedArray++;
    }
}
void merge(int a,int b)
{
    int x=parent[a];
    int y=parent[b];
    parent[x]=y;
}
int32_t main() {
    int t;
    cin>>t;
    for(int i=1;i<=t;i++)
    {
    int n;
    cin>>n;
    int k;
    cin>>k;
    int a[n];
    int sum=0;
    int sumaar[n+1]={0};
    for(int i=0;i<n;i++)
    {
        cin>>a[i];
        sum+=a[i];
    }
    
    
     sort(a,a+n);
     int j=0;
    for(int i=n-1;i>=0;i--)
    {
        j+=a[i];
        sumaar[i]=j;
       
    }
    
   /* for(int i=n-1;i>=0;i--)
    {
        cout<<sumaar[i]<<" ";
    }
    cout<<"\n";*/
    if(sum<=k)
    {
        cout<<0<<"\n";
        continue;
    }
    if(n==1)
    {
        cout<<a[0]-k<<"\n";
        continue;
    }
    int moves=sum-k;//dec anyone element by 1
    int totoalchangereqd=sum-k;
    int op1=INT_MAX;
    int y=0;
    for(int i=n-1;i>=1;i--)
    {
        y+=(a[i]-a[0]);
        if(y>=totoalchangereqd)
        {
          //  cout<<i<<" ";
            op1=n-i;
            break;
        }
    }
  //  cout<<op1<<" ";
    int d=sum-a[0];
    int left=0;
    int right=1e16;
    int ans=0;
    //itne se min dec karo a[0] ko so that n-1 ko a[0] ke equal kardo to sum<=k
    while(left<=right)
    {
        int mid=(left+right)/2;//itne se dec karenge
        if(mid>=a[0])
        {
        if(mid+d+((n-1)*(abs(a[0]-mid)))>=moves)
        {
            right=mid-1;
            ans=mid;
        }
        else 
        {
            left=mid+1;
        }
        }
        else 
        {
        if(mid+((n-1)*(abs(a[0]-mid)))>=moves)
        {
            right=mid-1;
            ans=mid;
        }
        else 
        {
            left=mid+1;
        }

        }
    }
    //cout<<"ans"<<ans<<" ";
    int decval=ans;
    int gh=0;
    int breakpoint=INT_MAX;
    for(int i=n-1;i>=1;i--)
    {
        gh+=a[i]-(a[0]-ans);
        if(gh+decval>=totoalchangereqd)
        {
            breakpoint=i;
            break;
        }
    }
    if(breakpoint==INT_MAX)
    {
        breakpoint=1;
    }
    int op2=ans+n-breakpoint;
    if(op2==n-1)
    {
        if((n*a[0])>k)
        {
            op2=INT_MAX;
        }
    }
    bool change=true;
    int ht=ans+1;
    int aagese=1;
    int ans3=INT_MAX;
   // cout<<"op2"<<op2<<"\n";
    stack<int>prevpos;
    prevpos.push(-1);
    //
    while(change&&aagese<n)
    {
        int decofarryazero=ht;
        int incinmoves=1;
       
        int left=aagese;
        int right=n-1;
        int pos=-1;
      //  cout<<"dec"<<decofarryazero<<" "<<left<<" "<<right<<"\n";
        while(left<=right)
        {
            int mid=(left+right)/2;
            if(decofarryazero>=a[0])
            {
            if((sumaar[mid]+(n-mid)*abs(a[0]-decofarryazero))>=abs(moves-decofarryazero))
            {
                pos=mid;
                left=mid+1;
            }
            else 
            {
                right=mid-1;
            }
            }
            else 
            {
               if(((n-mid)*abs(a[0]-decofarryazero))>=abs(moves-decofarryazero))
            {
                pos=mid;
                left=mid+1;
            }
            else 
            {
                right=mid-1;
            }
            }
        }
        
      //cout<<pos<<"\n";
       if(pos==-1)
       {
           ht++;
           aagese++;
           continue;
       }
        if(pos!=-1)
        {
        int sumofsuffix=sumaar[pos];
        if(decofarryazero>=a[0])
        {
        if((sumofsuffix+((n-pos)*abs(a[0]-decofarryazero))+decofarryazero)>=moves)
        {
            
            ans3=min(ans3,n-pos+decofarryazero);
            prevpos.push(pos);
           // cout<<"pp"<<ans3<<"\n";
        }
        else 
        {
            change=false;
        }
        }
        else 
        {
            if((((n-pos)*abs(a[0]-decofarryazero))+decofarryazero)>=moves)
        {
            
            ans3=min(ans3,n-pos+decofarryazero);
            prevpos.push(pos);
           // cout<<"pp"<<ans3<<"\n";
        }
        else 
        {
            change=false;
        }
        }
        }
        else 
        {
            change=false;
        }
        ht++;
        aagese++;


    }
    
    int finalasn=min(ans3,op2);
    int opp=min(moves,op1);
    
    cout<<min(opp,finalasn)<<"\n";
    }
}
/*
4
1 10
20
2 69
6 9
7 8
1 2 1 3 1 2 1
10 1
1 2 3 1 2 6 1 6 8 10

4
2 1
2 2
2 2 
2 2
3 1
2 2 2
5 1
2 2 2 2 2

1
5 3
1 1 1 1 4
5 2
1 3 1 1 1
5 3
1 1 1 1 3
5 4
1 1 3 1 1
5 5
1 1 3 1 1
5 6
1 1 3 1 1
5 7
1 1 1 1 3
5 1
1 1 1 1 4
5 2
1 4 1 1 1
5 3
1 1 1 1 4
5 4
4 1 1 1 1
5 5
1 1 1 1 4
5 6
2
2 1
2 2
2 2 
2 2
3 1
2 2 2
5 1
2 2 2 2 2

3
2
2
1
1
0
3
3
2
2
1
*/
