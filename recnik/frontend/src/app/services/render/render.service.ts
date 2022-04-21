import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TokenStorageService } from '../auth/token-storage.service';
import { Render } from '../../models';

@Injectable({
  providedIn: 'root',
})
export class RenderService {
  constructor(private httpClient: HttpClient, private tokenStorageService: TokenStorageService) {}

  getRenderi(): Observable<Render[]> {
    return this.httpClient.get<Render[]>('/api/render/dokument/');
  }

  getRender(id: number): Observable<Render> {
    return this.httpClient.get<Render>(`/api/render/dokument/${id}/`);
  }

  getRenderiZaObradjivaca(obradjivacId: number): Observable<any> {
    return this.httpClient.get<any>(`/api/render/odrednice/obradjivac/${obradjivacId}/`);
  }

  getRenderiSvi(): Observable<any> {
    return this.httpClient.get<any>(`/api/render/odrednice/sve/`);
  }

  download(render: Render): void {
    const filename = render.rendered_file.substring(render.rendered_file.lastIndexOf('/') + 1);
    const token = this.tokenStorageService.getAccessToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    this.httpClient.get(render.rendered_file, { headers, responseType: 'blob' as 'json'}).subscribe({
      next: (data: any) => {
        const dataType = data.type;
        const binaryData = [];
        binaryData.push(data);
        const blob = new Blob(binaryData, {type: dataType});
        const url = window.URL.createObjectURL(blob);
        const downloadLink = document.createElement('a');
        downloadLink.href = url;
        downloadLink.setAttribute('download', filename);
        document.body.appendChild(downloadLink);
        downloadLink.dispatchEvent(new MouseEvent(`click`, {bubbles: true, cancelable: true, view: window}));
        setTimeout(() => {
          document.body.removeChild(downloadLink);
          window.URL.revokeObjectURL(url);
        }, 100);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }
}
