<template>
  <div>
    <div id="dragover" @dragover="dragover" @drop="drop">
      <h3>Drag &amp; drop your file here</h3>
      <p>or <label for="file">click to browse</label></p>
      <input type="file" id="file" name="file" @change="selected">
    </div>
    <div>
    <span>{{ open }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: ['notify', 'n_file', 'addfile'],
  data () {
    return {
      name: null,
      pdf_file: null
    }
  },
  computed: {
    open () {
      if(this.n_file !== null) {
        this.getFile([this.n_file])
      }
    }
  },
  methods: {
    processReaderImage: function (readerData) {
      this.notify({
        name: this.name,
        src: readerData.target.result
      })
    },
    processReaderPDF: function (readerData) {
      this.notify({
        name: this.name,
        arrayBuffer: readerData.target.result
      })
    },
    getFile: function (fileList) {
      let file = fileList[0]
      let ch = this.addfile(file)
      if(!ch) {
        alert('already annoted file')
        return
      }
      this.name = file.name

      if (file.type.match('image.*')) {
        let reader = new FileReader()
        reader.addEventListener('load', this.processReaderImage, false)
        reader.readAsDataURL(file)
        this.pdf_file = file
      } else if (file.type.match('.*pdf.*')) {
        let reader = new FileReader()
        reader.addEventListener('load', this.processReaderPDF, false)
        reader.readAsArrayBuffer(file)
      } else {
        alert('Not a PDF or image file')
      }
    },
    selected: function (event) {
      this.getFile(event.target.files)
    },
    drop: function (event) {
      event.stopPropagation()
      event.preventDefault()
      this.getFile(event.dataTransfer.files)
    },
    dragover: function (event) {
      event.stopPropagation()
      event.preventDefault()
      event.dataTransfer.dropEffect = 'copy'
    }
  }
}
</script>

<style scoped>
div {
  text-align: center;
}

input {
  display: none;
}

p {
  font-size: 12px;
}

label {
  text-decoration: underline;
}

#dragover {
  background: #f1f1f1;
  border: solid #dedede 3px;
  padding: 20px 30px;
  margin-bottom: 30px;
}
</style>
