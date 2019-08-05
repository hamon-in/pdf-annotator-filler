<template>
  <div>
    <div class='selection-box' :style="styleObject">
      <span>{{ name }}</span>
    </div>
  </div>
</template>

<script>
import randomColor from 'randomcolor'

export default {
  name: 'area-select',
  props: ['coordinates', 'name', 'active', 'dimensions', 'pageoffset_top', 'pageoffset_left', 'open', 'keyid', 'highlight'],
  data () {
    return {
      color: randomColor({format: 'rgb'})
    }
  },
  computed: {
    styleObject: function () {
      if (this.height === 0 || this.width === 0) {
        return {
          display: 'none'
        }
      }
        if (this.coordinates.zname === this.highlight) {
          return {
            left: this.coordinates.left + this.coordinates.pageOffset_left - 1 + 'px',
            top: this.coordinates.top + this.coordinates.pageOffset_top - 4 + 'px',
            width: this.coordinates.width + 'px',
            height: this.coordinates.height + 'px',
            border: 'solid ' + this.color + ' 3px',
            background: this.color.replace(/\)$/, ', 0.05)').replace('rgb(', 'rgba(')
          }
        } else {
          return {
            left: this.coordinates.left + this.coordinates.pageOffset_left + 'px',
            top: this.coordinates.top + this.coordinates.pageOffset_top - 3 + 'px',
            width: this.coordinates.width + 'px',
            height: this.coordinates.height + 'px',
            border: 'solid ' + this.color + ' 1px',
            background: this.color.replace(/\)$/, ', 0.05)').replace('rgb(', 'rgba(')
          }
        }
    }
  }
}
</script>

<style scoped>

.selection-box {
  position: absolute;
  pointer-events: none;
  text-align: center;
  z-index: 1000;
  overflow:visible;
  word-break: break-all;
}

input {
 position: absolute;
 z-index: 2000;
}

span {
  top: 0em;
  overflow: visible;
  color: black;
  display: inline;
  font-size: 10px;
  text-shadow: white 0px 0px 2px, white 0px 0px 2px, white 0px 0px 5px, white 0px 0px 5px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 60px, white 0px 0px 60px, white 0px 0px 60px;
}

</style>
