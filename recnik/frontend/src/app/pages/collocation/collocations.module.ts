import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { CollocationsComponent } from './collocations.component';

import { ButtonModule } from 'primeng/button';
import { DeterminantModule } from '../determinant/determinant.module';
import { InputTextareaModule } from 'primeng/inputtextarea';

@NgModule({
  declarations: [CollocationsComponent],
  imports: [
    FormsModule,
    CommonModule,
    ButtonModule,
    InputTextareaModule,
    DeterminantModule,
  ],
  exports: [CollocationsComponent],
  providers: [],
  bootstrap: [CollocationsComponent],
})
export class CollocationsModule {}
