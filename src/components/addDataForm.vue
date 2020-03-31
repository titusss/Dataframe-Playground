 <!-- Main form for adding data tables/matrices --> 
 
 <template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">   
      <b-form-group id="input-group-4">
        <b-form-radio-group v-model="form.checked" id="checkboxes-4" required>
          <b-form-radio name="radio-category" value="RadioCategory">Category</b-form-radio>
          <div></div>
          <b-form-radio name="radio-table" value="RadioTable">Table</b-form-radio>
        </b-form-radio-group>
      </b-form-group>
      <b-form-group id="input-group-2" label="Title:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.name"
          required
          placeholder=""
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-1"
        label="From URL:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="url"
          required
          placeholder=""
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="From Database:" label-for="input-3">
        <b-form-select
          id="input-3"
          v-model="form.food"
          :options="foods"
          required
        ></b-form-select>
      </b-form-group>
      <b-form-group id="input-group-4" label="Upload File:" label-for="input-4" description="CSV, TSV, or Excel">
        <b-form-file accept=".csv, .txt, .tsv, .xlsx "></b-form-file>
      </b-form-group>
      <b-form-textarea
      id="textarea"
      v-model="text"
      placeholder="Or paste comma-seperated values here..."
      rows="3"
      max-rows="600"
    ></b-form-textarea>

    <pre class="mt-3 mb-0">{{ text }}</pre>
      <b-button type="submit" variant="primary">Add</b-button>
      <b-button type="reset" variant="danger" @click="$bvModal.hide('bv-modal-addData')">Cancel</b-button>
    </b-form>
    
  </div>
</template>


<script>
  export default {
    name: 'addDataForm',
    data() {
      return {
        form: {
          email: '',
          name: '',
          food: null,
          checked: []
        },
        text: '',
        foods: [{ text: 'Select One', value: null }, 'Carrots', 'Beans', 'Tomatoes', 'Corn'],
        show: true
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.name = ''
        this.form.food = null
        this.form.checked = []
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>