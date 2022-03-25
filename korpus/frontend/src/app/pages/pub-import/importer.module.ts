import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { FileUploadModule } from 'primeng/fileupload';
import { OrderListModule } from 'primeng/orderlist';
import { TimelineModule } from 'primeng/timeline';
import { ToolbarModule } from 'primeng/toolbar';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService } from 'primeng/api';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { PickListModule } from 'primeng/picklist';
import { DropdownModule } from 'primeng/dropdown';
import { InputTextModule } from 'primeng/inputtext';
import { RippleModule } from 'primeng/ripple';
import { MainImportComponent } from './main-import/main-import.component';
import { SelectFilesComponent } from './select-files/select-files.component';
import { ProcessStepComponent } from './process-step/process-step.component';
import { ExtractionComponent } from './extraction/extraction.component';
import { PreviewComponent } from './preview/preview.component';
import { MetadataComponent } from './metadata/metadata.component';

const routes: Routes = [
  {
    path: '',
    component: MainImportComponent,
    children: [{
      path: '',
      redirectTo: 'metapodaci',
      pathMatch: 'full'
    }, {
      path: 'metapodaci',
      component: MetadataComponent,
      data: { title: 'Метаподаци', mode: 'edit' }
    }, {
      path: 'datoteke',
      component: SelectFilesComponent,
      data: { title: 'Избор датотека' }
    }, {
      path: 'ekstrakcija',
      component: ExtractionComponent,
      data: { title: 'Издвајање текста' }
    }, {
      path: 'filteri',
      component: ProcessStepComponent,
      data: { title: 'Примена филтера' }
    }]
  }
];

@NgModule({
  declarations: [SelectFilesComponent, ProcessStepComponent, MainImportComponent, ExtractionComponent, PreviewComponent, MetadataComponent],
  imports: [
    CommonModule,
    FileUploadModule,
    OrderListModule,
    TimelineModule,
    ToolbarModule,
    ConfirmDialogModule,
    TableModule,
    TagModule,
    PickListModule,
    FormsModule,
    DropdownModule,
    InputTextModule,
    RippleModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  providers: [ConfirmationService],
  bootstrap: [MainImportComponent]
})
export class ImporterModule { }
