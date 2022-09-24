import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { PrilogComponent } from './prilog.component';

const routes: Routes = [{ path: '', component: PrilogComponent }]

@NgModule({
  declarations: [PrilogComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forRoot(routes),
    InputTextModule,
    MyToolbarModule,
  ],
  exports: [RouterModule],
  bootstrap: [PrilogComponent]
})
export class PrilogModule { }
