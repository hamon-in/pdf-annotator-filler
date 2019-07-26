<template>
    <div id="dragover" @dragover="dragover" @drop="drop" :style="{ position: 'relative' }">
      <h3>Drag &amp; drop your file here</h3>
      <p>or <label for="file">click to browse</label></p>
      <input type="file" id="file" name="file" @change="selected">
      <button @click="submit">submit</button>
    </div>
</template>


<script>
import { saveAs } from 'file-saver'



export default {
    props: ['u_key', 'pid'],
    data () {
        return {
            excel: null
        }
    },
    methods: {
        dragover (e) {
            e.stopPropagation()
            e.stopDefault()
            e.dataTransfer.dropEffect='copy'
        },
        drop (e) {
            e.stopPropagation()
            e.stopDefault()
            this.exel = e.dataTransfer.files[0]
        },
        selected (e) {
            this.excel = e.target.files[0]
        },
        async submit () {
            console.log(this.u_key)
            let data = new FormData()
            data.append('pid', this.pid)
            data.append('excel', this.excel)
            data.append('key', this.u_key)
            // await this.$http.post(`http://127.0.0.1:8500/upload/create`, data, {
            //     headers: {
            //         'Content-Type': 'multipart/form-data'
            //     }
            // }).then((data) => {
            //     console.log(data)
            // })
            let dat = await this.$http.post(`http://127.0.0.1:8500/pdf/fill/${this.pid}?key=${this.u_key}`, data, {
                headers: {
                    'Content-Type': 'multipart-formdata'
                }
            })
            // data = await data.blob()
            console.log(dat)
            data = await fetch(`http://127.0.0.1:8500/zip/${dat.body.path}/pdf.zip`)
            data = await data.blob()
            let filesaver = require('file-saver')
            filesaver.saveAs(data,'folder.zip')
        }
    }
}
</script>

<style>
    #dragover {
        background-color: tan;
        border: solid #dedede 3px;
        padding: 20px 30px;
        margin-bottom: 30px;
        width: 400px;
    }
</style>
