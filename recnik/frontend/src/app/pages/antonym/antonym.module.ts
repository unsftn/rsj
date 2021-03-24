import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { ButtonModule } from 'primeng/button';
import { DeterminantModule } from '../determinant/determinant.module';
import { AntonymComponent } from './antonym.component';

@NgModule({
  declarations: [AntonymComponent],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    AutoCompleteModule,
    ButtonModule,
    DeterminantModule,
  ],
  exports: [AntonymComponent],
  providers: [],
  bootstrap: [AntonymComponent],
})
export class AntonymModule {}
