// Routing aid only: native KiCad DRC remains mandatory. C++17.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 if(argc!=3)return 2;
 string prefix=argv[1];ifstream cfg(prefix+".txt");int nx,ny,ns,ng;cfg>>nx>>ny>>ns>>ng;int N=nx*ny,sz=2*N;vector<int>starts(ns),goals(ng);for(auto&x:starts)cfg>>x;for(auto&x:goals)cfg>>x;
 vector<uint8_t> m(sz),v(sz);for(int l=0;l<2;l++){ifstream a(prefix+"-m"+to_string(l)+".raw",ios::binary),b(prefix+"-v"+to_string(l)+".raw",ios::binary);a.read((char*)m.data()+l*N,N);b.read((char*)v.data()+l*N,N);if(!a||!b)return 3;}
 vector<int> dist(sz,INT32_MAX),prev(sz,-1);vector<uint8_t>target(sz,0),closed(sz,0);for(int g:goals)target[g]=1;
 auto h=[&](int id){int z=id%N,x=z%nx,y=z/nx,res=INT32_MAX;for(int g:goals){g%=N;int dx=abs(x-g%nx),dy=abs(y-g/nx);res=min(res,10*max(dx,dy)+4*min(dx,dy));}return res;};
 using Q=array<int,3>;priority_queue<Q,vector<Q>,greater<Q>>q;for(int s:starts){dist[s]=0;q.push({h(s),0,s});}int found=-1,expanded=0;
 while(!q.empty()){
  auto [f,c,id]=q.top();q.pop();if(c!=dist[id]||closed[id])continue;closed[id]=1;if(target[id]){found=id;break;}expanded++;int l=id/N,z=id%N,x=z%nx,y=z/nx;
  auto add=[&](int j,int weight){if(closed[j]||m[j])return;int nc=c+weight;if(nc<dist[j]){dist[j]=nc;prev[j]=id;q.push({nc+h(j),nc,j});}};
  for(int dy=-1;dy<=1;dy++)for(int dx=-1;dx<=1;dx++){if(!(dx||dy))continue;int xx=x+dx,yy=y+dy;if(xx<0||xx>=nx||yy<0||yy>=ny)continue;if(dx&&dy&&(m[l*N+y*nx+xx]||m[l*N+yy*nx+x]))continue;add(l*N+yy*nx+xx,dx&&dy?14:10);}
  if(!v[z]&&!v[N+z])add((1-l)*N+z,650);
 }
 ofstream out(argv[2]);if(found<0){cerr<<"NO_PATH "<<expanded<<"\n";return 4;}
 // Existing vias are represented by starts/goals on both connected layers.
 for(int id=found;id>=0;id=prev[id])out<<id<<"\n";
 cerr<<"ROUTED "<<expanded<<" cost "<<dist[found]<<"\n";return 0;
}
