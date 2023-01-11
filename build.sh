#清缓存
sync
echo 3 > /proc/sys/vm/drop_caches
#重启前端
cd vue-admin-template/
#安装依赖
#npm install --registry=https://registry.npm.taobao.org
#设置环境变量
export NODE_OPTIONS=--openssl-legacy-provider
#打包前端
npm run build:stage