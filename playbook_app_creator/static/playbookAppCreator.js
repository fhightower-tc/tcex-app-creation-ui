Vue.component('new-input', {
    template: `
        <div>
            <form>
                <input type="text" name="variable name">
            </form>
            {{ name }}
            <button class="button">Add input</button>
        </div>
    `,
    data () {
      return {
        name: 'test'
      };
    },
});

var playbookAppVue = new Vue({
    el: "#content",
    data: {
        inputs: [],
        output: [],
    },
    methods: {
        addInput: function() {
            this.inputs.push("1");
        }
    }
});