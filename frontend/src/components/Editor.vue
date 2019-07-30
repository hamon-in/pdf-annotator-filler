<template>
<div>
  <div class='login' v-if='login'>
    <button id='l' v-if='signin' class='btn' @click='f_signin(false,true,true,null)'>signup</button>
    <button id='l' v-if='signup' class='btn' @click='f_signin(true,false,true,null)'>signin</button>
    <signup :f_signin="f_signin" v-if='signup'></signup>
    <signin :f_signin="f_signin" v-if='signin'></signin>
  </div>
  <div v-else>
    <button class='btn' @click="advanced_reset">signout</button>
      <div class='editor'>
        <div class='sidebar'>
          <h1>PDF - Annotator</h1>
          <Uploader v-if="open < 3" v-show="open < 1" :n_file="n_file" :addfile="addfile" :notify="newFile"></Uploader>
          <div v-if="open < 2">
            <PDFZoneViewer @updateob="updateobj" :dimensions="pdfDimensions" :selections="selections" class='zone-viewer' :batchUpdateSelections="batchUpdateSelections" :originalFilename="name" v-if="arrayBuffer"></PDFZoneViewer>
          </div>
          <div v-if="open < 3">
            <div v-if="open < 2">
            <div v-for="(o_i, o_ind) in old_obs" :key="o_ind">
              <div v-if="o_ind ===  o_editid">
                <input type="text" :value="o_i.zname" @keyup.13="o_edit(o_i,$event)">
              </div>
              <div v-else>
                {{ o_i.zname }}
                <div v-if="o_ind === change_an && change_st">
                  {{ f_change_an(o_i) }}
                </div>
                <button class='btn' @click="o_editid = o_ind">edit</button>
                <button id='r' class='btn' @click="o_del(o_ind) ">x</button>
                <button class='btn' @click="change_an = o_ind">change</button>
              </div>
            </div>
            <div v-for="(i, ind) in obs" :key="old_obs.length + ind">
              <input type="text" :value="i.zname" @mouseleave="highlight=null" @mouseover="highlight=i.zname" @keyup.13="edit(i,$event)" :can="true">
              <button id='r' class='btn' @click="del(ind)">x</button>
            </div>
            <div>
              <input v-if='sed || sde || scre' class='btn' @click="poost" value='submit' type='submit'>
            </div>
            </div>
              <button class='btn' v-if="open === 0" @click="get(3)">
                <center>open</center>
              </button> 
              <button class='btn' v-if="open === 1 || open === 2" @click="adv_reset(false,open+=2)">back</button>
          </div>
          <div v-else>
            <div v-for="(file,i) in saved_files" :key=i>
              {{ file.pname }}
              <button class='btn' @click="file_open(file,open-2)"> open </button>
            </div>
            <button class='btn' v-if="open === 3" @click="adv_reset(false,0)">
                <center>back</center>
            </button> 
          </div>
        </div>
          <div v-if="open < 3" class='content'>
            <Annotator :highlight="highlight" :getcan="getcan" :znamech="znamech" :open="open" :old_obs="old_obs" :pageoffset="pageoffset" :dimensions="pdfDimensions" :obs="obs" :src="src" :setPdfSize="setPdfSize" :arrayBuffer="arrayBuffer" :name="name" :selections="selections" :addSelection="addSelection"></Annotator>
          </div>
      </div>
  </div>
</div>
</template>

<script>
import Uploader from '@/components/Uploader'
import Annotator from '@/components/Annotator'
import ZoneViewer from '@/components/ZoneViewer'
import PDFZoneViewer from '@/components/PDFZoneViewer'
import randomColor from 'randomcolor'
import signin from '@/components/signin'
import signup from '@/components/signup'
import filler from '@/components/filler'

function initialise() {
  return {
    purpose: true,
    signup: false,
    signin: true,
    login: true,
    n_file: null,
    highlight: null,
    can: false,
    sdel: false,
    sed: false,
    scre: false,
    del_obs: [],
    ed_obs: [],
    zname: '',
    open: 0,
    change_st: false,
    ch_cordinates: null,
    change_an: null,
    editid: null,
    o_editid: null,
    pageoffset: null,
    c: 0,
    pid: null,
    style: [],
    old_obs: [],
    req1_stat: false,
    file: null,
    obs: [],
    src: null,
    arrayBuffer: null,
    name: '',
    selections: [],
    pdfDimensions: {
      height: 0,
      width: 0
    }
  }
}

export default {
  name: 'editor',
  components: {
    Uploader,
    Annotator,
    ZoneViewer,
    PDFZoneViewer,
    signup,
    signin,
    filler
  },
  data () {
    return {...initialise(), ...{key: null, saved_files: []}}
  },
  created () {
    console.log('Editor created')
    console.log(this.pdfDimensions)
  },
  methods: {
    advanced_reset () {
      Object.assign(this.$data,{...initialise(), ...{key: null, saved_files: this.saved_files}})
    },
    adv_reset (p,o) {
      Object.assign(this.$data, {...initialise(), ...{key: this.key, saved_files: this.saved_files}})
      this.login = false
      this.purpose = p
      this.open = o
    },
    async file_open(file,o) {
      this.open = o
      let filename = file.pname
      console.log(filename)

      let data = await fetch(`http://0.0.0.0:8500/${filename}`,{
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      console.log(data)
      data = await data.blob()
      console.log(data)
      data['name'] = file.pname
      this.n_file = data
      data = await this.$http.get(`http://0.0.0.0:8500/pdf/${file.pid}?key=${this.key}`)
      
      this.pid = data.body.pid
      this.old_obs = data.body.zones
          console.log(this.n_file)
          this.annotation = true
    },
    f_purpose (o) {
      this.open = o
      this.purpose = false
    },
    async f_signin (i,u,l,key) {
      this.signup = u
      this.signin = i
      this.login = l
      this.purpose = true
      this.key = key
      if(!l) 
      {
        let data = await this.$http.get(`http://0.0.0.0:8500/pdf?key=${key}`)
        console.log(data)
        if(data !== undefined) {
          this.saved_files = data.body
        }
          console.log(this.saved_files)
      }
    },
    getcan (data) {
      this.can = data
    },
    znamech (data) {
      this.zname = data
    },
    f_change_an (d) {
      d.left = this.ch_cordinates.left
      d.top = this.ch_cordinates.top
      d.width = this.ch_cordinates.width
      d.height = this.ch_cordinates.height
      d.pageOffset_left = this.ch_cordinates.pageOffset_left
      d.pageOffset_top = this.ch_cordinates.pageOffset_top
      d.pageno = this.ch_cordinates.pageno
      console.log(d)
      this.sed = true
      let n = this.ed_obs.find(x => x.id === d.id)
      if (!n) {
        this.ed_obs = [...this.ed_obs, d]
      }
      this.change_an = null
      this.ch_cordinates = null
      console.log(d)
      console.log(this.ed_obs)
      this.change_st = false
    },
    del (i) {
      this.obs.splice(i, 1)
      console.log(this.obs)
    },
    o_del (i) {
      let del = this.old_obs.splice(i, 1)
      this.del_obs = [...this.del_obs, del[0].zid]
      this.sdel = true
      console.log(this.del_obs)
    },
    o_edit (d, event) {
      console.log(event.target.value)
      d.zname = event.target.value
      this.sed = true
      let n = this.ed_obs.find(x => x.id === d.id)
      if (!n) {
        this.ed_obs = [...this.ed_obs, d]
      }
      console.log(this.ed_obs)
      this.o_editid = null
    },
    edit (d, event) {
      console.log(event.target.value)
      d.zname = event.target.value
    },
    addfile (file) {
      console.log(this.saved_files)
      this.file = file
      if(this.open === 0) {
        if (this.saved_files.some((item) => item.pname === file.name)) {
          this.file = null
          return 0
        }
      }
      return 1
     
    },
    async get (o) {
      this.arrayBuffer = null
        this.open = o
    },
    post () {
      if (this.change && this.open ===0) {
        let data = new FormData()
        data.append('pfile', this.file)
        data.append('key',this.key)
        this.req1_stat = true
        this.$http.post('http://0.0.0.0:8500/pdf/create',
        data,
          {
            headers: {
              'Content-Type': 'multipart/form-data' 
            }
          }, function (data, status, request) {
            this.postResults = data
            this.ajaxRequest = false
          }).then(function (data) {
            console.log(data)
            console.log('wait finished')
            this.pid = data.body.pid
            this.change = false
            this.req1_stat = false
            this.saved_files = [...this.saved_files, data.body]
            this.poost()
          }).catch(function (data) {
            console.log('From catch')
          })
          return 0
      }
    },
    poost () {
      this.post()
      if (!this.req1_stat) {
        if (this.scre) {
          this.$http.post('http://0.0.0.0:8500/zone/create', {
            pid: this.pid,
            zones: this.obs,
            key: this.key
          }, {
            headers: {
              'content-type': 'application/json'
            }
          }).then(function (data) {
            console.log(data)
            console.log('finished')
            console.log([...this.old_obs, ...this.obs])
            this.old_obs = [...this.old_obs, ...data.body]
            console.log(this.old_obs)
            this.obs = []
            this.scre = false
          })
        }
        if (this.sed) {
          this.$http.put('http://0.0.0.0:8500/zone/update', { zones: this.ed_obs,key: this.key }, {
            headers: {
              'content-type': 'application/json'
            }
          }).then(function (data) {
            console.log(data)
            console.log(this.obs)
            console.log('edit finished')
            this.ed_obs = []
            this.sed = false
          })
        }
        if (this.sdel) {
          console.log(this.del_obs)
          this.$http.delete('http://0.0.0.0:8500/zone/delete', {body: { zids: this.del_obs,key: this.key }}).then(function (data) {
            console.log(data)
            console.log(this.obs)
            console.log('delete finished')
            this.del_obs = []
            this.sdel = false
          })
        }
      }
    },
    updateobj (data) {
      this.obs = data
    },
    batchUpdateSelections: function (selections) {
      this.selections = selections
    },
    setPdfSize: function (width, height) {
      this.pdfDimensions = {
        width: width,
        height: height
      }
      console.log(width, height)
    },
    addSelection: function (coords) {
      if (coords.height === 0 || coords.width === 0) {
        return
      }
      if (this.change_an === null) {
        this.selections.push({
          id: +new Date(),
          coordinates: {
            top: coords.top,
            left: coords.left,
            height: coords.height,
            width: coords.width,
            page: coords.page,
            pageOffset_left: coords.pageOffset_left,
            pageOffset_top: coords.pageOffset_top
          },
          color: randomColor({format: 'rgb'}),
          name: 'Box' + this.selections.length
        })
        this.pageoffset = coords.pageOffset
        this.obs = [...this.obs, {
          zname: this.zname,
          top: coords.top,
          left: coords.left,
          height: coords.height,
          width: coords.width,
          pageno: coords.page,
          pageOffset_top: coords.pageOffset_left,
          pageOffset_left: coords.pageOffset_top,
          canvas_width: this.can[coords.page - 1].width,
          canvas_height: this.can[coords.page - 1].height
        }]
        console.log(this.obs)
        this.scre = true
        this.c++
        this.style.push({
          id: this.c
        })
      } else {
        this.ch_cordinates = {
          zname: this.zname,
          top: coords.top,
          left: coords.left,
          height: coords.height,
          width: coords.width,
          pageno: coords.page,
          pageOffset_left: coords.pageOffset_left,
          pageOffset_top: coords.pageOffset_top
        }
        this.change_st = true
      }
    },
    newFile: function (data) {
      console.log('newfile')
      if (this.name === data.name) {
        this.change = false
      } else {
        this.change = true
      }
      this.name = data.name
      this.src = data.src
      this.arrayBuffer = data.arrayBuffer
      this.selections = []
      this.obs = []
      this.old_obs = []
      this.del_obd = []
      this.ed_ob = []
      this.scre = false
      this.sdel = false
      this.sed = false
      this.style = []
      this.c = 0
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.editor {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  margin-top: 60px;
}

.sidebar {
  position: relative;
  width: 400px;
  top: 0;
  left: 0;
  padding: 10px;
  align-content: center
}

.filler {
  position: relative;
  width: 400px;
  top: 0;
  left: 0;
  padding: 10px;
  align-content: center
}

.content {
  position: absolute;
  width: auto;
  margin-left: 30px;
  top: 0px;
  left: 410px;
}

textarea {
  -webkit-box-sizing: border-box;
   -moz-box-sizing: border-box;
        box-sizing: border-box;
  font-size: 1em;
}

h2 {
  background: #FFF800;
  padding: 10px 25px;
}

h1 {
  background: #C50080;
  padding: 10px 25px;
  color: white;
}

select {
  position: relative;
  z-index: 100;
}

.login {
  top: 10em;
  position: relative;
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px 0 30px 0;
  box-sizing: border-box;
  float: left;
  width: 50%;
  margin: auto;
  padding: 0 50px;
  margin-top: 6px;
  left: 18em;
  text-align: center;
}

.btn {
  padding: 12px;
  border: none;
  border-radius: 4px;
  margin: 5px 0;
  opacity: 0.85;
  display: inline-block;
  font-size: 17px;
  line-height: 0px;
}

input:hover,
.btn:hover {
  opacity: 1;
}

input[type=submit] {
  background-color: #4CAF50;
  height: 2rem;
  width: 5rem;
  color: white;
  cursor: pointer;
  align-items: center;
  text-align: center;
  display: inline-block;
  padding: 0px;
}

#r {
  width: 0.5em;
  height: 0.5em;
  border-radius: 100%;
  text-align: center;
}

#l{
  width: 100%;
  line-height: 20px;
  
}

input[type=text], select {
  width: 50%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

</style>
