import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileUploadModule } from 'primeng/fileupload';
import { OrderListModule } from 'primeng/orderlist';
import { TimelineModule } from 'primeng/timeline';
import { SelectFilesComponent } from './select-files/select-files.component';
import { ProcessStepComponent } from './process-step/process-step.component';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'datoteke',
    component: SelectFilesComponent,
    data : {
      title: 'Избор датотека'
    }
  }
];

@NgModule({
  declarations: [SelectFilesComponent, ProcessStepComponent],
  imports: [
    CommonModule,
    FileUploadModule,
    OrderListModule,
    TimelineModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
})
export class ImporterModule { }
