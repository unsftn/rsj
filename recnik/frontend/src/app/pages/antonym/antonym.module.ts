import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { AntonymComponent } from './antonym.component';

import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';

@NgModule({
  declarations: [AntonymComponent],
  imports: [FormsModule, DropdownModule, CommonModule, ButtonModule],
  exports: [AntonymComponent],
  providers: [],
  bootstrap: [AntonymComponent],
})
export class AntonymModule {}
