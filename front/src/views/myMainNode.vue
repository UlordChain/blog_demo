<template>
<div class="mainNode-container" v-if="!loading">

    <div class="content-container">
      <h2 class="mainNode-title">主节点管理</h2>
        <!-- 主节点申请 start -->
        <div v-if="status == 3">
          <div class="tip-wrap" v-if="!real">
            <h4>提示：</h4>
            <p>
              您还未实名认证，请进行
              <router-link to="/personal/realNameAuth" class="back-rna">实名认证</router-link>
            </p>
          </div>
          <div class="apply-wrap">
            <h4 class="apply-title">主节点申请</h4>
            <el-form name="mainNode" :model="mainNodeForm"  ref="mainNodeForm" :rules="mainNodeFormRules" class="apply-form-wrap">
                <el-form-item prop="value2" label="主节点类型">
                  <el-select v-model="mainNodeForm.value2" placeholder="主节点类型" popper-class="nodeTypeSelect-wrap">
                    <el-option
                      v-for="item in options2"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                      class="nodeTypeSelect">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item prop="intro" label="主节点竞选简介">
                  <el-input v-model="mainNodeForm.intro" type="textarea" class="mainNode-input-large" maxlength="100" placeholder="填写主节点竞选简介"></el-input>
                </el-form-item>
                <el-form-item prop="fileUrl" label="申请材料附件">
                  <div class="filename"> {{mainNodeForm.fileName}}</div>
                    <el-upload
                      class="upload"
                      ref="upload"
                      action="https://upload.qiniup.com/"
                      :auto-upload="false"
                      :data = "aaa"   
                      :show-file-list="false"
                      :on-success="handleAvatarSuccess"
                      :before-upload="beforeAvatarUpload"
                       :on-change="handleChangeUpload"
                      :on-progress="uploadFileProcess">
                      <div class="upload-btn">上传附件</div>

                    </el-upload>
                    <el-progress v-if="fileFlag == true " type="circle" :percentage="Number(fileUploadPercent.percentage.toFixed(0))" style="margin-top:30px;"></el-progress>
                      <a style="margin-left: 6px;" href="../static/Ulord.zip" download="Ulord.zip" class="download-word">下载申请模板</a>
                      <div class="fileTip">附件格式为docx或pdf，不大于5MB</div>
                  </el-form-item>
                  <el-form-item prop="extraUrl" label="额外申请材料链接">
                    <el-input v-model="mainNodeForm.extraUrl" placeholder="填写申请材料链接" class="mainNode-input-large" maxlength="320"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary"  @click.prevent.native="submit" class="mainNode-submit-btn">申请</el-button>
                  </el-form-item>
            </el-form>
          </div>
          <div class="mainNode-faq-container">
                        <h2>常见问题</h2>
                        <div class="faq-wrap">
                          <h4 class="question">
                            什么是主节点?
                          </h4>
                          <div class="answer">
                            <p class="paragraph">
                              在Ulord网络中，主节点系统组成稳定的骨干网络，保障网络通信以及交易的实时验证，同时组成一个海量的存储、计算资源池并提供一些其他基础服务，满足Ulord网络的内容分发多样化的应用场景，保证高质量的网络存储，提供更优质的视频流和数据流服务。
                            </p>
                            <p class="paragraph">
                              Ulord考虑不同的应用场景，对主节点系统做了充分的设计，既考虑了主节点的服务质量，又考虑服务的类别与激励的个体差异，真正将主节点系统打造成功能完备的分布式计算集群。同时，通过引入主节点候选机制，Ulord系统将对主节点提供的各种服务的质量进行考核，淘汰一些不满足要求的主节点。
                            </p>
                          </div>
                        </div>
                        <div class="faq-wrap">
                          <h4 class="question">
                            主节点类型和功能?
                          </h4>
                          <div class="answer">
                            <p>主节点根据所提供的主要服务具体可分为五大类，具体如下：</p>
                            <p>1、应用服务型主节点（简称应用型主节点）</p>
                            <p>主要负责承载Ulord公链钱包、区块浏览器、DNS解析及网关等服务；</p>
                            <p>2、存储服务型主节点（简称储存型主节点）</p>
                            <p>主要用来部署UDFS服务，对外提供分布式存储服务，这是白皮书中提到的最基本的主节点类型；</p>
                            <p>3、计算服务型主节点（简称计算型主节点）</p>
                            <p>侧重提供分布式计算服务，包括深度学习，大数据处理，高性能计算等；</p>
                            <p>4、基础服务型主节点（简称荣誉型主节点）</p>
                            <p>提供最基础的全节点服务，为Ulord社区做运营推广，如资源对接和项目推广等，扩大Ulord影响力；</p>
                            <p>5、共识服务型主节点（简称共识型主节点）</p>
                            <p>提供超级账户服务，提供高吞吐的区块链服务器。</p>
                            <p>针对不同类型的服务器，Ulord系统对主节点服务器的要求也有所不同。</p>
                          </div>
                        </div>
                      </div>
                      <!-- 主节点须知弹出框 start -->
                      <el-dialog
                        title="主节点申请条款"
                        :visible.sync="dialogVisible"
                        :before-close="handleClose"
                        :close-on-click-modal="popup"
                        :close-on-press-escape="popup">
                        <div class="clause-container">
                            <div class="clause-wrap">
                                <h4>一、主节点的义务</h4>
                                <p>
                                  对Ulord系统内的资源和站点进行审查，维护Ulord生态健康有序发展；对开发者提出的预案进行评估，推进社区对Ulord的贡献。对Ulord项目宣传推广相关的活动，如线下分享活动、社区治理、线上活动组织和扩大影响力等等。
                                </p>
                                <h4>二、 主节点的权力</h4>
                                <p>
                                  主节点拥有Ulord提案的投票权以及PoS收益权。从区块高度57600开始至210239，每个区块中主节点收益为52个UT，出块时间与PoW普通区块一致。第一期每月激励：52UT/块*576块/天*30天 ÷节点数，更详细的收益计算见对应专题。
                                </p>
                                <h4>三、主节点的风险</h4>
                                <p>
                                  3.1 主节点的收益波动
                                </p>
                                <p>
                                  主节点的收益与网络中的主节点个数有关，每一个块都会按规则选定一个主节点发放奖励，主节点的收益存在一定的波动。
                                </p>
                                <p>
                                  3.2 主节点的政策风险
                                </p>
                                <h4>四、主节点的资格回收</h4>
                                <p>
                                  4.1 主节点服务质量过低
                                </p>
                                <p>
                                  主节点服务质量长时间过低会被取消主节点资格，主节点拥有者需要按照规定选择符合标准的硬件配置搭建主节点。
                                </p>
                                <p>
                                  4.2 未履行主节点申请的承诺
                                </p>
                                <p>
                                  主节点拥有者需履行主节点申请时做出的承诺，否则Ulord基金会有权收回主节点资格。
                                </p>
                                <p>
                                  4.3 政策变更
                                </p>
                                <p>
                                  主节点遵守国家相关法律法规，若违反国家相关法律条例Ulord基金会有权收回主节点资格。
                                </p>
                                <h4>五、授予Ulord社区主节点代投权</h4>
                                <p>
                                  主节点拥有Ulord的发展决议权对Ulord的关键提案进行投票，您在Ulord社区绑定您的主节点时会赋予Ulord社区提案代投权，代投权仅在您未进行提案投票时有效，拥有代投权也无法更改您已进行了投票的提案。
                                </p>
                                <h4>六、主节点的隐私须知</h4>
                                <p>
                                  主节点进程会收集主节点的运行情况及硬件信息进行收益计算及去中心化的组织主节点网络。
                                </p>
                            </div>
                            <div class="check-wrap">
                                <el-checkbox v-model="checked">我已阅读并接受《主节点申请条款》</el-checkbox>
                            </div>
                            <div class="clause-btn-wrap">
                                <el-button type="primary"  :disabled="!checked" @click="checked = true; dialogVisible =false" class="clause-btn-ok">同意</el-button>
                            </div>
                        </div>
                      </el-dialog>
                      <!-- 主节点须知弹出框 end -->

        </div>
        <!-- 主节点申请 end -->
        <!-- 申请已提交 start -->
        <div v-if="status == 0" class="submited-wrap">
          <div class="submited-title">
            <i class="el-icon-circle-check submited-icon"></i>
            <span>主节点申请已提交</span>
          </div>
          <div class="submited-content">已经收到您的申请，我们会尽快审核并向您反馈结果。</div>
        </div>
        <!-- 申请已提交 end -->
        <!-- 申请已通过 start -->
        <div v-if="status == 1">
          <div class="state-passed-container">
              <div class="passed-content">
                  <h2 class="passed-tip">
                    <i class="el-icon-circle-check"></i>
                    恭喜，您的申请已通过
                  </h2>
              </div>
          </div>
          <div class="bind-content-wrap">
            <h4 class="bind-content-title">绑定主节点</h4>
            <el-form name="mainNodeBind" :model="mainNodeBindForm" :rules="mainNodeBindFormRules"  ref="mainNodeBindForm">
              <el-form-item prop="nickName">
                <span class="form-ItemTitle nmnStar">主节点昵称</span>
                <el-input v-model="mainNodeBindForm.nickName" maxlength="10" placeholder="主节点昵称仅支持字母和数字"></el-input>
              </el-form-item>
              <el-form-item prop="tradeTxid">
                <span class="form-ItemTitle nmnStar">1万UT押金交易ID</span>
                <el-input v-model="mainNodeBindForm.tradeTxid" @input="checkNo3(mainNodeBindForm.tradeTxid)" maxlength="64"></el-input>
              </el-form-item>
              <el-form-item prop="tradeVoutNo">
                <span class="form-ItemTitle nmnStar">1万UT押金Vout索引</span>
                <el-select v-model="mainNodeBindForm.tradeVoutNo" placeholder="0">
                  <el-option label="0" value="0"></el-option>
                  <el-option label="1" value="1"></el-option>
                </el-select>
                <!-- <el-input v-model="mainNodeBindForm.tradeVoutNo" @input="checkNo4(mainNodeBindForm.tradeVoutNo)" type="tel" maxlength="10" ></el-input> -->
              </el-form-item>
              <el-form-item >
                <span class="form-ItemTitle">主节点类型</span>
                <span class="mainNode-type">{{nodeType | node}}</span>
              </el-form-item>
              <el-form-item prop="ipAddress">
                <span class="form-ItemTitle nmnStar">主节点IP</span>
                <el-input v-model="mainNodeBindForm.ipAddress" @input="checkNo2(mainNodeBindForm.ipAddress)" maxlength="20"></el-input>
              </el-form-item>
              <el-form-item prop="specialCode">
                <span class="form-ItemTitle nmnStar">主节点特征码</span>
                <el-input type="text"  maxlength="64" @input="checkNo(mainNodeBindForm.specialCode)" v-model="mainNodeBindForm.specialCode"></el-input>
              </el-form-item>
              <el-form-item>
                <span class="form-ItemTitle"></span>
                <el-button type="primary" @click.prevent.native="submitMainNode" class="mainNode-submit-btn">绑定</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <!-- 申请已通过 end -->
        <!-- 申请未通过 start-->
          <div v-if="status == 2">
        <div class="state-fail-container2">
          <div class="fail-content">
            <h2 class="fail-tip">
              <i class="el-icon-error"></i> 
              <span class="error-tip1">差一点就通过了</span>
              <span class="error-tip2">过一段时间您可以重新提交申请材料,若有疑问请发送邮件至 ulorder@ulord.one 联系官方工作人员。</span>
            </h2>
            <!-- <div class="fail-modification">
                    您可以
                    <router-link to="/changeNodeIP" class="modification">重新申请</router-link>
                  </div> -->
              <div class="fail-more">
                <div>
                  您还可以做这些提高通过几率：
                </div>
                 <div>
                  <i class="el-icon-success"></i> 为Ulord作出自己的贡献
                </div>
                 <div>
                  <i class="el-icon-success"></i> 丰富您的个人资料
                </div>
              </div>
              <div style="text-align: center; margin-top: 18px;">
                <el-button @click="returnIndex" type="primary">返回用户中心</el-button>
              </div>
          </div>
        </div>
      </div>
        <div v-if="status == 4" class="passed-wrap">
          <div class="state-passed-container">
              <div class="passed-content">
                  <h2 class="passed-tip">
                    <i class="el-icon-circle-check"></i>
                    恭喜，您已绑定主节点
                  </h2>
              </div>
          </div>
          <div class="ran-info-wrap">
            <span>国籍: </span>
            <div>{{bindInfo.authenticationVo.nationality}}</div>
          </div>
          <div class="ran-info-wrap">
            <span>姓名: </span>
            <div>{{bindInfo.authenticationVo.name}}</div>
          </div>
          <div class="ran-info-wrap">
            <span>证件号: </span>
            <div>{{bindInfo.authenticationVo.certificateNo}}</div>
          </div>
          <div class="ran-info-wrap">
            <span>手机号: </span>
            <div>{{bindInfo.authenticationVo.phone}}</div>
          </div>
          <!-- <div class="ran-info-wrap">
            <span>主节点IP: </span>
            <div>{{bindInfo.majorNodeBindVo.ipAddress}}</div>
          </div> -->
          <div class="ran-info-wrap">
            <span>主节点IP: </span>
            <div>{{bindInfo.majorNodeBindVo.ipAddress}}</div>
          </div>
          <div class="ran-info-wrap">
            <span>1万UT交易抵押地址: </span>
            <div class="input-height">{{utAddress}}
              
            </div>
            <i class="el-icon-refresh icon-re" @click="refreshAddress" v-show="!bindInfo.majorNodeBindVo.utAddr">没有收到地址？</i>
          </div>
          <div class="ran-info-wrap">
            <span>证书: </span>
            <div class="input-height">{{bindInfo.majorNodeBindVo.certificate}}</div>
          </div>
          <!-- <div class="ran-info-wrap">
            <span>证书有效时间: </span>
            <div class="input-height">{{bindInfo.majorNodeBindVo.certificate}}</div>
          </div> -->
        </div>
        <div v-if="status == 5" class="state-fail-container">
          <div class="fail-content">
                  <h2 class="fail-tip">
                  <i class="el-icon-success"></i>
                  同步证书需要一点时间
                </h2>
                <div class="fail-reply">
                  您可以先逛逛提案和任务模块
                </div>
                <div class="fail-modification">
                  您可以
                  <router-link to="/" class="modification">去逛逛</router-link>
                </div>
            </div>
        </div>
        <div v-if="status == 6">
          修改页面
          <el-button @click="submit">提交</el-button>
          <el-button @click="cancel">取消修改</el-button>
        </div>

      </div>

</div>
</template>

<script>
import {
  getNodeInfo,
  getMainNode,
  getMainNodeInfo,
  getBindMainNode,
  bindMainNode,
  checkMainName,
  getQiToken,
  getUtAddress
} from "@/api/api";
import { getToken } from "@/utils/auth";
import { validateURL, validateMainName, txId, ip } from "@/utils/validate";
import { apiUrl } from "@/api/url";
import store from "../store";
export default {
  data() {
    const validateAbstract = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请填写申请主节点简介"));
      } else if (value.length > 100) {
        callback(new Error("简介限制100字符内"));
      } else {
        callback();
      }
    };
    const validateExtraUrl = (rule, value, callback) => {
      if (!value) {
        callback();
      } else if (value.length > 320) {
        callback(new Error("链接长度最大不超过320字符"));
      } else if (!validateURL(value)) {
        callback(new Error("请填写正确的链接"));
      } else {
        callback();
      }
    };
    const validateNickName = (rule, value, callback) => {
      if (!value) {
        callback(new Error("主节点昵称不能为空"));
      } else if (value.length > 10 || value.length < 2) {
        callback(new Error("主节点昵称称限制在2-10字符内"));
      } else if (!validateMainName(value)) {
        callback(new Error("请输入正确的主节点昵称"));
      } else if (value && validateMainName(value)) {
        checkMainName(value).then(res => {
          if (!res.success) {
            callback(new Error("主节点名称已存在"));
          } else {
            callback();
          }
        });
      } else {
        callback();
      }
    };
    const validateTxId = (rule, value, callback) => {
      console.log(value);
      if (!value) {
        callback(new Error("请输入特征码"));
      } else if (!txId(value)) {
        callback(new Error("请输入正确的特征码"));
      } else {
        // else if (value.length != 64) {
        //   callback(new Error("请输入正确的交易id"));
        // }
        callback();
      }
    };
    const validateIp = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入ip地址"));
      } else if (ip(value)) {
        callback(new Error("请输入正确的ip地址"));
      } else {
        callback();
      }
    };
    const validateVoutNo = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入索引值"));
      } else {
        callback();
      }
    };
    const validateCode = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入交易ID"));
      } else if (!txId(value)) {
        callback(new Error("请输入正确的交易id"));
      } else {
        callback();
      }
    };
    const validateSCode = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入特征码"));
      } else if (!txId(value)) {
        callback(new Error("请输入正确的特征码"));
      } else {
        callback();
      }
    };

    return {
      status: 0,
      downloadUrl: apiUrl,
      url: apiUrl + "/api/fileOperations/uploadFile.Action",
      checked: false, //点击同意协议按钮
      popup: false, //禁止点击取消弹框
      optionD: false,
      fileFlag: false,
      dialogVisible: true,
      real: store.getters.real,
      loading: true,
      nodeType: 0,
      bindInfo: null,
      utAddress: "",
      mainNodeForm: {
        value2: "",
        intro: "",
        fileUrl: "",
        fileName: "",
        extraUrl: ""
      },
      mainNodeBindForm: {
        nickName: "",
        tradeTxid: "",
        tradeVoutNo: 0,
        ipAddress: "",
        specialCode: ""
      },
      mainNodeFormRules: {
        value2: [
          { required: true, trigger: "change", message: "请选择节点类型" }
        ],
        intro: [
          { required: true, trigger: "blur", validator: validateAbstract }
        ],
        fileUrl: [{ required: true, trigger: "blur", message: "请上传附件" }],
        extraUrl: [{ trigger: "blur", validator: validateExtraUrl }]
      },
      mainNodeBindFormRules: {
        nickName: [
          { required: true, trigger: "blur", validator: validateNickName }
        ],
        tradeTxid: [
          { required: true, trigger: "blur", validator: validateCode }
        ],
        ipAddress: [{ required: true, trigger: "blur", validator: validateIp }],
        specialCode: [
          { required: true, trigger: "blur", validator: validateSCode }
        ]
      },
      headerData: {
        client_name: "jwt",
        token: getToken()
      },
      aaa: {},
      options2: [
        {
          value: "0",
          label: "应用型"
        },
        // {
        //   value: "1",
        //   label: "存储型"
        // },
        // {
        //   value: "2",
        //   label: "计算型"
        // },
        {
          value: "3",
          label: "荣誉型"
        }
        // {
        //   value: "4",
        //   label: "共识型"
        // }
      ]
    };
  },
  filters: {
    node(type) {
      if (type == 0) {
        return "应用型";
      } else if (type == 1) {
        return "存储型";
      } else if (type == 2) {
        return "计算型";
      } else if (type == 3) {
        return "荣誉型";
      } else if (type == 4) {
        return "共识型";
      }
    }
  },
  methods: {
    returnIndex() {
      this.$router.push("/personal/personalInfo");
    },
    refreshAddress() {
      getUtAddress().then(res => {
        console.log("123");
        if (res.success) {
          this.utAddress = res.utAddress;
        }
      });
    },
    checkNo(value) {
      let reg = /^[1-9]\d*$/;
      if (value) {
        if (value > 999999 || new RegExp(reg).test(value) == false) {
          setTimeout(() => {
            this.mainNodeBindForm.specialCode = this.mainNodeBindForm.specialCode.replace(
              /\W/g,
              ""
            );
          }, 100);
        }
      }
    },
    checkNo2(value) {
      let reg = /^[1-9]\d*$/;
      if (value) {
        if (value > 999999 || new RegExp(reg).test(value) == false) {
          setTimeout(() => {
            this.mainNodeBindForm.ipAddress = this.mainNodeBindForm.ipAddress.replace(
              /[^\d.]/g,
              ""
            );
          }, 100);
        }
      }
    },
    checkNo3(value) {
      let reg = /^[1-9]\d*$/;
      if (value) {
        if (value > 999999 || new RegExp(reg).test(value) == false) {
          setTimeout(() => {
            this.mainNodeBindForm.tradeTxid = this.mainNodeBindForm.tradeTxid.replace(
              /\W/g,
              ""
            );
          }, 100);
        }
      }
    },
    checkNo4(value) {
      let reg = /^[1-9]\d*$/;
      if (value) {
        if (value > 999999 || new RegExp(reg).test(value) == false) {
          setTimeout(() => {
            this.mainNodeBindForm.tradeVoutNo = this.mainNodeBindForm.tradeVoutNo.replace(
              /\W/g,
              ""
            );
          }, 100);
        }
      }
    },

    handleClose(done) {
      done();
    },
    //绑定主节点
    submitMainNode() {
      this.$refs.mainNodeBindForm.validate(valid => {
        if (valid) {
          bindMainNode(
            this.mainNodeBindForm.nickName,
            this.mainNodeBindForm.tradeTxid,
            this.mainNodeBindForm.tradeVoutNo,
            this.mainNodeBindForm.ipAddress,
            this.mainNodeBindForm.specialCode
          ).then(res => {
            if (res.success) {
              location.reload();
            } else if (res.errorCode == "100017") {
              this.$message({
                message: "交易id已存在，请重新填写",
                type: "error"
              });
            } else if (res.errorCode == "200001") {
              this.$message({
                message: "ip地址不正确",
                type: "error"
              });
            }
          });
        }
      });
    },
    //上传成功
    handleAvatarSuccess(res, file) {
      this.mainNodeForm.fileName = file.name;
      this.mainNodeForm.fileUrl = res.url + "?attname=" + file.name;
      this.$refs.mainNodeForm.validateField("fileUrl", filUrl => {});
    },

    //上传前
    beforeAvatarUpload(file) {
      const isLt5M = file.size / 1024 / 1024 < 5;
      const extension1 =
        file.name.substr(file.name.length - 3, 3) === "doc" ||
        file.name.substr(file.name.length - 4, 4) === "docx";
      const extension2 = file.name.substr(file.name.length - 3, 3) === "pdf";
      if (!extension1 && !extension2) {
        this.$message.error("上传文件只能是 doc,docx,pdf 格式!");
        return false;
      } else if (!isLt5M) {
        this.$message.error("上传文件大小不能超过 5MB!");
        return false;
      } else {
        return true;
      }
    },
    handleChangeUpload(file) {
      getQiToken(file.name).then(res => {
        if (res.success) {
          this.aaa = {
            token: res.token
          };
          setTimeout(this.uploadAction, 500);
        } else {
          return false;
        }
      });
    },
    uploadAction() {
      this.$refs.upload.submit();
    },
    //上传中
    uploadFileProcess(event, file, fileList) {
      console.log(file.percentage);
      this.fileFlag = true;
      this.fileUploadPercent = file;
      console.log(file);
    },
    verify() {
      this.status = 6;
    },
    binda() {
      this.status = 7;
    },
    //获取主节点类型
    getNode() {
      var that = this;
      getNodeInfo().then(function(res) {
        if (res.success) {
          for (var item in res.map) {
            that.options2.push({
              value: item,
              label: res.map[item]
            });
          }
        }
      });
    },
    cancel() {
      this.getBindMain();
    },

    //获取主节点申请状态
    getInfo() {
      this.loading = true;
      getMainNodeInfo().then(res => {
        console.log(res);
        if (res.errorCode == "100003" || res.errorCode == "100008") {
          //没申请
          this.status = 3;
          this.loading = false;
        } else {
          if (res.majorNodeApplyVo.status == 0) {
            this.status = 0; //申请审核中
            this.loading = false;
          } else if (res.majorNodeApplyVo.status == 1) {
            this.status = 1; //通过审核
            this.nodeType = res.majorNodeApplyVo.nodeType;
            this.loading = false;
          } else if (res.majorNodeApplyVo.status == 2) {
            this.status = 2; //审核失败
            this.loading = false;
          }
        }
      });
    },

    //获取主节点绑定状态
    getBindMain() {
      console.log("213");
      this.loading = true;
      getBindMainNode().then(res => {
        if (res.errorCode == "100003" || res.errorCode == "100008") {
          //没绑定
          this.getInfo();
          console.log("没绑定");
        } else if (
          res.majorNodeBindDetailsVo.majorNodeBindVo.hasOwnProperty(
            "certificate"
          )
        ) {
          //绑定了，查询绑定信息
          this.status = 4; //审核通过，证书已经发放
          this.bindInfo = res.majorNodeBindDetailsVo;
          if (
            res.majorNodeBindDetailsVo.majorNodeBindVo.hasOwnProperty("utAddr")
          ) {
            this.utAddress = res.majorNodeBindDetailsVo.majorNodeBindVo.utAddr;
          }
          this.loading = false;
          console.log(this.status, "状态");
        } else {
          this.status = 5; //绑定还在审核中
          this.loading = false;
          console.log(this.status, "绑定完");
        }
      });
    },
    //提交申请
    submit() {
      if (!store.getters.real) {
        this.$confirm("您还未进行实名认证", "提示", {
          confirmButtonText: "去认证",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            this.$router.push("/personal/realNameAuth");
          })
          .catch(() => {});
      }
      this.$refs.mainNodeForm.validate(valid => {
        if (valid) {
          getMainNode(
            this.mainNodeForm.fileUrl,
            this.mainNodeForm.extraUrl,
            this.mainNodeForm.intro,
            this.mainNodeForm.value2
          ).then(res => {
            if (res.success) {
              this.$message({
                message: "提交申请成功",
                type: "success"
              });
              location.reload();
            }
          });
        }
      });
    },
    bind() {}
  },
  mounted() {
    this.getBindMain();
    this.getNode();
  },
  beforeCreate() {
    document.querySelector("body").setAttribute("style", "background:#f4f4f4");
  },
  beforeDestroy() {
    document.querySelector("body").setAttribute("style", "");
  }
};
</script>
<style rel="stylesheet/scss" lang="scss">
.mainNode-container {
  .upload {
    display: inline-block;
  }
  .el-progress {
    margin: 0 !important;
  }
  .icon-re {
    margin-left: 10px;
    cursor: pointer;
    font-size: 16px;
    position: absolute;
    bottom: 2px;
    color: #999999;
  }
  .el-progress-circle {
    margin: 0 !important;
    width: 46px !important;
    height: 46px !important;
  }
  .el-progress--circle .el-progress__text {
    top: 80%;
  }
  .el-progress__text {
    font-size: 12px;
  }
  .el-form-item__content * {
    vertical-align: middle;
    height: 44px;
  }
  // ------主节点申请弹出框 start ------
  .el-dialog {
    width: 670px;
    height: 788px;
    border-radius: 12px;
    margin-top: 8vh !important;
    box-shadow: transparent;
  }
  .el-dialog__header {
    padding: 0;
  }
  .el-dialog__title {
    font-size: 18px;
    color: #444444;
    text-align: center;
    padding: 25px 0;
    border-bottom: 1px solid #ebebeb;
    display: block;
  }
  .el-dialog__headerbtn .el-dialog__close {
    display: none;
  }
  .el-dialog__body {
    padding: 0;
  }
  .clause-container {
    .clause-wrap {
      height: 573px;
      overflow-y: scroll;
      padding: 0 15px;
      h4 {
        font-size: 16px;
        color: #444444;
        margin: 20px 0;
        text-align: justify;
        line-height: 24px;
        word-wrap: break-word;
      }
      p {
        font-size: 14px;
        color: #666666;
        text-align: justify;
        line-height: 24px;
        word-wrap: break-word;
      }
    }
    .check-wrap {
      text-align: center;
      margin: 20px 0;
      font-size: 14px;
    }
    .el-checkbox__input.is-checked + .el-checkbox__label {
      color: #666666;
    }
    .el-checkbox__input.is-checked .el-checkbox__inner,
    .el-checkbox__input.is-indeterminate .el-checkbox__inner {
      background-color: #4f81f4;
      border-color: #4f81f4;
    }
    .clause-btn-wrap {
      margin: 0 auto;
      text-align: center;
    }
    .clause-btn-ok {
      background: #4f81f4;
      width: 100px;
      height: 44px;
      line-height: 44px;
      padding: 0;
      font-size: 14px;
      color: #ffffff;
      border: none;
    }

    /* 滚动条 */
    ::-webkit-scrollbar-track-piece {
      background-color: #f8f8f8;
    }
    ::-webkit-scrollbar {
      width: 5px;
      height: 30px !important;
    }
    ::-webkit-scrollbar-thumb {
      height: 30px !important;
      background: #cacaca;
      border-radius: 100px;
      background-clip: padding-box;
    }
  }

  .input-height {
    height: auto !important;
    word-wrap: break-word;
    line-height: 2 !important;
  }
  // ------主节点申请弹出框 end ------
  .apply-form-wrap {
    .el-form-item__label {
      width: 145px;
      font-size: 14px;
      color: #999999;
      display: inline-block;
      text-align: left;
      vertical-align: middle;
    }
    .el-form-item__content {
      margin: 0 auto;
      width: 953px;
      line-height: 44px;
    }
    .el-form-item {
      .form-ItemTitle {
        font-size: 14px;
        color: #999999;
        display: inline-block;
        vertical-align: middle;
        width: 181px;
        line-height: 44px;
        -moz-user-select: none;
        user-select: none;
        text-align: left;
      }
      .mainNode-submit-btn {
        background: #4f81f4;
        width: 100px;
        height: 44px;
        line-height: 44px;
        padding: 0;
        font-size: 14px;
        color: #ffffff;
        border: none;
        margin-left: 145px;
      }
    }
    .nmnStar::after {
      content: "*";
      color: red;
      vertical-align: top;
    }
    .el-input__inner {
      width: 280px;
      height: 44px;
      line-height: 44px;
      background: #f4f4f4;
      font-size: 14px;
      color: #666666;
    }
    .mainNode-input-large {
      width: 600px;
      .el-input__inner {
        width: 100%;
        height: 44px;
        line-height: 44px;
        background: #f4f4f4;
      }
    }
    // 文本域 start
    .el-textarea {
      width: 600px;
      display: inline-block;
    }
    .el-textarea__inner {
      min-height: 44px !important;
      padding: 10px 15px 0;
      font-size: 14px;
      color: #666666;
      background: #f4f4f4;
      border: 1px solid #dddddd;
      border-radius: 4px;
    }
    // 文本域 end
  }
}

// ------选择下拉框 start------
.el-popper .popper__arrow {
  display: none;
}
.el-popper[x-placement^="bottom"] {
  margin-top: 0;
}
.nodeTypeSelect-wrap {
  border: none;
  box-shadow: 0 2px 4px 0 rgba(210, 210, 210, 0.5);
  margin-top: 10px !important;
  .el-select-dropdown__list {
    padding: 0;
  }
  .nodeTypeSelect {
    font-size: 14px;
    color: #282828;
    height: 44px;
    line-height: 44px;
    padding: 0 15px !important;
  }
  .nodeTypeSelect.selected {
    font-size: 14px;
    color: #d37015;
    font-weight: normal;
    height: 44px;
    line-height: 44px;
  }
  .nodeTypeSelect.hover,
  .nodeTypeSelect:hover {
    background: #f2f2f2;
    font-size: 14px;
    color: #282828;
    height: 44px;
    line-height: 44px;
  }
  .el-select-dropdown {
    top: 300px !important;
    z-index: 2 !important;
  }
}
.el-icon-arrow-up:before {
  content: "\E60C";
  color: #999999;
}
// ------选择下拉框 end------
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.mainNode-container {
  background-color: #f4f4f4;
  // 申请已提交
  .submited-wrap {
    padding-bottom: 263px;
    .submited-title {
      margin: 0 auto;
      padding-top: 110px;
      text-align: center;
      .submited-icon {
        font-size: 24px;
        color: #6bc00c;
      }
      span {
        font-size: 20px;
        color: #444444;
        vertical-align: bottom;
      }
    }
    .submited-content {
      font-size: 16px;
      color: #666666;
      text-align: center;
      margin-top: 28px;
    }
  }
  .passed-wrap {
    margin: 0 auto;
    text-align: center;
    padding-bottom: 100px;
    .passed-title {
      margin: 0 auto;
      padding-top: 33px;
      text-align: center;
      margin-bottom: 42px;
      .passed-icon {
        font-size: 24px;
        color: #4f81f4;
      }
      span {
        font-size: 20px;
        color: #444444;
        vertical-align: bottom;
      }
    }
    .ran-info-wrap {
      position: relative;
      margin-bottom: 20px;
      span {
        width: 145px;
        font-size: 14px;
        color: #999999;
        display: inline-block;
        text-align: left;
        vertical-align: middle;
      }
      div {
        display: inline-block;
        background: #f4f4f4;
        border-radius: 4px;
        width: 320px;
        height: 44px;
        line-height: 44px;
        padding: 0 18px;
        text-align: left;
        vertical-align: middle;
      }
    }
  }
  .upload-btn {
    display: inline-block;
    width: 100px;
    height: 44px;
    font-size: 14px;
    color: #ffffff;
    background: #4f81f4;
    border-radius: 4px;
    margin-right: 10px;
  }
  .download-word {
    font-size: 14px;
    color: #4f81f4;
  }

  .container {
    width: 1200px;
    margin: 0 auto;
  }
  .content-container {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 4px;
  }
  /*====================================
                主节点申请
  =====================================*/
  .mainNode-title {
    border-bottom: 1px solid #ebebeb;
    border-radius: 4px;
    width: 100%;
    margin: 0 auto;
    text-align: center;
    padding: 26px 0;
    font-size: 18px;
    color: #444444;
  }
  .tip-wrap {
    width: 100%;
    height: 144px;
    border-bottom: 1px solid #ebebeb;
    h4 {
      font-size: 18px;
      color: #444444;
      letter-spacing: 0.48px;
      padding: 30px 0 17px 92px;
    }
    p {
      font-size: 14px;
      color: #a9a9b3;
      letter-spacing: 0.37px;
      line-height: 28px;
      padding-left: 112px;
      .back-rna {
        font-size: 14px;
        color: #000000;
        letter-spacing: 0.33px;
        line-height: 28px;
      }
    }
  }
  .apply-wrap {
    width: 100%;
    border-bottom: 1px solid #ebebeb;
    padding-left: 92px;
    box-sizing: border-box;
    .apply-title {
      font-size: 18px;
      color: #444444;
      padding: 29px 0 40px 0;
    }
  }
  // 常见问题 start
  .mainNode-faq-container {
    width: 100%;
    margin: 0 auto;
    padding-bottom: 143px;
    h2 {
      font-size: 18px;
      color: #444444;
      letter-spacing: 0.48px;
      padding: 30px 0 32px 92px;
    }
    .faq-wrap {
      .question {
        font-size: 16px;
        color: #444444;
        letter-spacing: 0.43px;
        margin-bottom: 20px;
        margin-left: 113px;
      }
      .answer {
        font-size: 14px;
        color: #666666;
        letter-spacing: 0.37px;
        text-align: justify;
        line-height: 24px;
        padding: 0 110px 40px 112px;
        word-wrap: break-word;
      }
    }
  }
  // 常见问题 end
  .filename {
    width: 280px;
    display: inline-block;
    padding: 0 15px;
    border-radius: 4px;
    margin-right: 10px;
    height: 44px;
    line-height: 44px;
    background: #f4f4f4;
    border: 1px solid #dddddd;
    color: #606266;
    box-sizing: border-box;
  }
  .fileTip {
    font-size: 14px;
    color: #a9a9b3;
    margin-left: 145px;
  }
  /*====================================
            主节点绑定
  =====================================*/

  .bind-title {
    border-bottom: 1px solid #ebebeb;
    border-radius: 4px;
    width: 100%;
    margin: 0 auto;
    text-align: center;
    padding: 26px 0;
    font-size: 18px;
    color: #444444;
  }
  .bind-content-wrap {
    width: 100%;
    border-bottom: 1px solid #ebebeb;
    padding-left: 92px;
    box-sizing: border-box;
    .bind-content-title {
      font-size: 18px;
      color: #444444;
      padding: 29px 0 40px 0;
    }
    .el-form-item__content {
      margin: 0 auto;
      width: 953px;
      line-height: 44px;
    }
    .el-form-item {
      .form-ItemTitle {
        font-size: 14px;
        color: #999999;
        display: inline-block;
        vertical-align: middle;
        width: 181px;
        line-height: 44px;
        -moz-user-select: none;
        user-select: none;
        text-align: left;
      }
      .mainNode-submit-btn {
        background: #4f81f4;
        width: 100px;
        height: 44px;
        line-height: 44px;
        padding: 0;
        font-size: 14px;
        color: #ffffff;
      }
    }
    .nmnStar::after {
      content: "*";
      color: red;
      vertical-align: top;
    }
    .el-input__inner {
      width: 280px;
      height: 44px;
      line-height: 44px;
      background: #f4f4f4;
      font-size: 14px;
      color: #666666;
    }
    .mainNode-input-large {
      width: 767px;
      .el-input__inner {
        width: 100%;
        height: 44px;
        line-height: 44px;
        background: #f4f4f4;
      }
    }
    .el-input {
      width: 280px;
    }
    .mainNode-type {
      font-size: 14px;
      color: #666666;
    }
  }

  /*====================================
            申请已通过
  =====================================*/
  .state-passed-container {
    .passed-title {
      border-bottom: 1px solid #ebebeb;
      border-radius: 4px;
      width: 100%;
      margin: 0 auto;
      text-align: center;
      padding: 26px 0;
      font-size: 18px;
      color: #444444;
    }
    .passed-content {
      .passed-tip {
        font-size: 20px;
        color: #444444;
        letter-spacing: 0.53px;
        text-align: center;
        margin: 26px 0 30px;
        font-weight: bold;
        i {
          font-size: 24px;
          color: #4f81f4;
          margin-right: 4px;
          vertical-align: bottom;
        }
      }
      // 表单 start
      .el-form-item__content {
        margin: 0 auto;
        width: 393px;
        line-height: 44px;
      }
      .el-form-item {
        margin-bottom: 20px;
        .form-ItemTitle {
          font-size: 14px;
          color: #999999;
          display: inline-block;
          vertical-align: middle;
          width: 108px;
          line-height: 44px;
          -moz-user-select: none;
          user-select: none;
          text-align: left;
        }
      }
      .el-input {
        width: 280px;
      }
      .el-input__inner {
        width: 280px;
        height: 44px;
        line-height: 44px;
        background: #f4f4f4;
        font-size: 14px;
        color: #666666;
      }
      // 表单 end
      .bind-btn {
        background: #4f81f4;
        width: 100px;
        height: 44px;
        line-height: 44px;
        padding: 0;
        font-size: 14px;
        color: #ffffff;
        display: inline-block;
      }
    }
  }
  /*====================================
            申请已提交
  =====================================*/
  .state-committed-container {
    .committed-title {
      border-bottom: 1px solid #ebebeb;
      border-radius: 4px;
      width: 100%;
      margin: 0 auto;
      text-align: center;
      padding: 26px 0;
      font-size: 18px;
      color: #444444;
    }
    .committed-content {
      padding-bottom: 270px;
      .committed-tip {
        font-size: 20px;
        color: #444444;
        letter-spacing: 0.53px;
        text-align: center;
        margin: 37px 0 28px;
        font-weight: bold;
        i {
          font-size: 24px;
          color: #6bc00c;
          margin-right: 4px;
          vertical-align: bottom;
        }
      }
      .committed-reply {
        font-size: 16px;
        color: #666666;
        margin: 0 auto;
        text-align: center;
        margin-bottom: 20px;
      }
      .committed-modification {
        font-size: 14px;
        color: #a9a9b3;
        text-align: center;
        .modification {
          font-size: 14px;
          color: #000000;
          text-align: center;
          line-height: 21px;
          &:hover {
            color: #d37015;
          }
        }
      }
    }
  }

  /*====================================
            申请未通过
  =====================================*/
  .state-fail-container {
    .fail-title {
      border-bottom: 1px solid #ebebeb;
      border-radius: 4px;
      width: 100%;
      margin: 0 auto;
      text-align: center;
      padding: 26px 0;
      font-size: 18px;
      color: #444444;
    }
    .fail-content {
      padding-bottom: 270px;
      .fail-tip {
        font-size: 20px;
        color: #444444;
        letter-spacing: 0.53px;
        text-align: center;
        margin: 37px 0 28px;
        font-weight: bold;
        i {
          font-size: 24px;
          color: rgb(82, 196, 26);
          margin-right: 4px;
          vertical-align: bottom;
        }
      }
      .fail-reply {
        font-size: 16px;
        color: #666666;
        margin: 0 auto;
        text-align: center;
        margin-bottom: 20px;
      }
      .fail-modification {
        font-size: 14px;
        color: #a9a9b3;
        text-align: center;
        .modification {
          font-size: 14px;
          color: #000000;
          text-align: center;
          line-height: 21px;
          &:hover {
            color: #d37015;
          }
        }
      }
    }
  }
  .state-fail-container2 {
    .fail-title {
      border-bottom: 1px solid #ebebeb;
      border-radius: 4px;
      width: 100%;
      margin: 0 auto;
      text-align: center;
      padding: 26px 0;
      font-size: 18px;
      color: #444444;
    }
    .fail-more {
      box-sizing: border-box;
      padding-left: 146px;
      & > div {
        margin-bottom: 14px;
      }
      i {
        color: green;
      }
    }
    .fail-content {
      padding-bottom: 270px;
      .fail-tip {
        text-align: center;
        margin: 37px 0 28px;
        .error-tip1 {
          font-size: 20px;
          display: inline-block;
          margin: 18px 0;
        }
        .error-tip2 {
          font-size: 16px;
          display: block;
          color: #666666;
        }
        i {
          display: block;
          margin: 18px 0;
          font-size: 66px;
          margin-right: 4px;
          vertical-align: bottom;
          color: rgb(234, 34, 45);
        }
      }
      .fail-reply {
        font-size: 16px;
        color: #666666;
        margin: 0 auto;
        text-align: center;
        margin-bottom: 20px;
      }
      .fail-modification {
        font-size: 14px;
        color: #a9a9b3;
        text-align: center;
        .modification {
          font-size: 14px;
          color: #000000;
          text-align: center;
          line-height: 21px;
          &:hover {
            color: #d37015;
          }
        }
      }
    }
  }
}
</style>
