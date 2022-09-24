import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { TabViewModule } from 'primeng/tabview';
import { FieldsetModule } from 'primeng/fieldset';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { PridevComponent } from './pridev.component';

const routes: Routes = [{ path: '', component: PridevComponent }]

@NgModule({
  declarations: [PridevComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forRoot(routes),
    InputTextModule,
    TabViewModule,
    FieldsetModule,
    MyToolbarModule,
  ],
  exports: [RouterModule],
  bootstrap: [PridevComponent]
})
export class PridevModule { }
