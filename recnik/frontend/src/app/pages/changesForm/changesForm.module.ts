import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { ChangesFormComponent } from './changesForm.component';

import { TableModule } from 'primeng/table';

@NgModule({
  declarations: [ChangesFormComponent],
  imports: [FormsModule, CommonModule, TableModule],
  exports: [ChangesFormComponent],
  providers: [],
  bootstrap: [ChangesFormComponent],
})
export class ChangesFormModule {}
