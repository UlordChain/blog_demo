<template>
  <el-row :gutter="20">
    <el-col :span="4">
      <div class="grid-content"></div>
    </el-col>
    <el-col :span="16">
      <div class="grid-content list-home bg-purple">
        <div class="list-header">
          <h3>Ulord博客</h3>
          <router-link to="/info" class="mc info">个人中心</router-link>
          <router-link to="/publish" class="mc publish">发布</router-link>
        </div>
        <div class="list-content" v-if="loading">
          <div class="content-wrap">
            <div class="item-blog">
              <div class="item" v-for="item in data.msg.list" :key="item.index">
                <h4 class="item-title">
                  {{item.title || '暂无'}}
                  <span v-if="item.type ==2 " class="abc">广告</span>
                  <span v-if="item.udfs" class="abc">已购买</span>
                </h4>
                <div class="item-main">
                  <p class="intro">
                    {{item.description || '暂无'}} </p>
                </div>
                <div class="price">{{item.price || '暂无'}}SUT</div>
                <div class="author">发布地址：{{item.author || '暂无'}}</div>
                <div class="more" @click="goDetail(item.udfs, item.claim_id, item.author, item.price, item.type)">
                  查看更多
                </div>
              </div>
            </div>
          </div>
          <div class="block">
            <span class="demonstration"></span>
            <el-pagination layout="prev, pager, next" :current-page="listQuery.page" :total="data.msg.total" @current-change="handleCurrentChange">
            </el-pagination>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="4">
      <div class="grid-content"></div>
    </el-col>
  </el-row>
</template>

<script>
import { getToken, removeToken } from "@/utils/auth";
export default {
  name: "articleList",
  data() {
    return {
      data: null,
      loading: false,
      token: getToken(),
      listQuery: {
        page: 1
      }
    };
  },
  methods: {
    getList() {
      console.log("123");
      this.data = Web3Helper.queryResourceList(this.token, this.listQuery.page);
      if(this.data.result == 0) {
        removeToken();
        location.reload();
      }
      this.loading = true;
    },
    buy(id, address, price) {
      Web3Helper.purchaseResource(this.token, id, address, price, 2000000000);
    },
    goDetail(udfs, id, address, price, type) {
      if (type == 2) {
        this.$router.push({ path: "/article", query: { id: id } });
      } else {
        if (udfs) {
          this.$router.push({ path: "/article", query: { id: id } });
        } else {
          this.buy(id, address, price);
        }
      }
    },
    handleCurrentChange(val) {
      console.log(val);
      this.listQuery.page = val;
      this.getList();
    }
  },
  mounted() {
    this.getList(1);
  }
};
</script>

<style lang="scss" scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #fff;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.list-home {
  .list-header {
    position: relative;
    h3 {
      display: inline-block;
    }
  }
  .mc {
    padding: 10px;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
  .info {
    right: 0px;
  }
  .publish {
    right: 90px;
  }
  .content-wrap {
    min-height: 700px;
  }
  .item {
    padding: 0 0 18px 0;
    border-bottom: 1px solid #eee;
    border-top: 1px solid #eee;
    .price {
      display: inline-block;
    }
    .more {
      cursor: pointer;
      text-align: right;
    }
    .abc {
      margin-left: 10px;
      display: inline-block;
      font-weight: normal;
      font-size: 12px;
      padding: 2px;
      border: 1px solid #444;
      border-radius: 4px;
    }
  }
}
</style>
